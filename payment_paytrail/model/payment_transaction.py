# -*- coding: utf-8 -*-
import json
import logging
import pprint
import uuid

from werkzeug import urls

from odoo import models, fields, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """Override of payment to return Paytrail-specific rendering values."""

        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'paytrail':
            return res

        endpoint = '/payments'
        payload = self._paytrail_prepare_payment_request_payload()
        _logger.info("sending '/payments' request for link creation:\n%s", pprint.pformat(payload))
        payment_data = self.provider_id._paytrail_make_request(endpoint, payload)

        print('API Response', payment_data)

        # The provider reference is set now to allow fetching the payment status after redirection
        self.provider_reference = payment_data.get('id')

        checkout_url = payment_data['href']
        return {'api_url': checkout_url}

    def _paytrail_prepare_payment_request_payload(self):
        """Generate payload for Paytrail payment request."""
        amount_in_cents = round(self.currency_id._convert(
            self.amount,
            self.env['res.currency'].search([("name", "=", "EUR")]),
            self.env.company,
            fields.Date.today()
        ) * 100)
        if amount_in_cents < 1:
            _logger.error("Paytrail Error: Amount must be greater than 0. Current value: %s", amount_in_cents)
            raise ValidationError(_("Payment amount must be at least 0.01 EUR."))

        base_url = self.get_base_url()
        redirect_url = urls.url_join(base_url,'/payment/paytrail/return')

        body = {
            "stamp": str(uuid.uuid4()),
            "reference": self.reference,
            "amount": int(amount_in_cents),
            "currency": "EUR",
            "language": "EN",
            "items": [
                {
                    "unitPrice": int(amount_in_cents),
                    "units": 1,  # Quantity
                    "vatPercentage": 0,
                    "productCode": "#1234",
                    "deliveryDate": str(fields.Date.today()),
                }
            ],
            "customer": {"email": self.partner_email},
            "redirectUrls": {"success": redirect_url, "cancel": redirect_url},
        }
        return json.dumps(body, separators=(',', ':'))



    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Find the transaction based on the notification data.

          For a provider to handle transaction processing, it must overwrite this method and return
          the transaction matching the notification data.

          :param str provider_code: The code of the provider handling the transaction.
          :param dict notification_data: The notification data sent by the provider.
          :return: The transaction, if found.
          :rtype: recordset of `payment.transaction`
          """
        print('-------------------------------------')
        print('Comes inside the _get_tx of PAYTRAIL')
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'paytrail' or len(tx) == 1:
            print("NOO")
            return tx
        print("YES")
        tx = self.search(
            [('reference', '=', notification_data.get('checkout-reference')), ('provider_code', '=', 'paytrail')]
        )
        if not tx:
            print("NO tx")
            raise ValidationError("Paytrail: " + _(
                "No transaction found matching reference %s.", notification_data.get('checkout-reference')
            ))
        print('tx Present ,', tx)

        return tx

    def _process_notification_data(self, notification_data):
        """ Override of payment to process the transaction based on Mollie data.

        Note: self.ensure_one()

        :param dict notification_data: The notification data sent by the provider
        :return: None
        """
        print('-------------------------------------')
        print('Comes inside the _pro_notification of PAYTRAIL')
        super()._process_notification_data(notification_data)

        if self.provider_code != 'paytrail':
            return
        payment_status = notification_data.get('checkout-status')
        if payment_status in ['pending', 'delayed']:
            self._set_pending()
        elif payment_status == 'ok':
            print('STATUS IS OK')
            self._set_done()
        elif payment_status in ['fail']:
            self._set_canceled("Paytrail: " + _("Cancelled payment with status: %s", payment_status))
        else:
            _logger.info(
                "received data with invalid payment status (%s) for transaction with reference %s",
                payment_status, self.reference
            )
            self._set_error(
                "Paytrail: " + _("Received data with invalid payment status: %s", payment_status)
            )