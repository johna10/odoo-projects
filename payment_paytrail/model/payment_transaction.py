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

    # def _get_specific_processing_values(self, processing_values):
    #     """overriding payment and adding logic for custom payment method"""
    #     res = super()._get_specific_processing_values(processing_values)
    #     if self.provider_code != 'paytrail':
    #         return res
    #     payload = self._paytrail_prepare_payment_request_payload()
    #     payment_response = self.provider_id._paytrail_make_request(payload)
    #     self.provider_reference = payment_response.get('reference')
    #     redirect_form_html = self.env['ir.qweb']._render('payment_paytrail.redirect_form_paytrail', {
    #         'payment_url': payment_response['href'],
    #     })
    #     processing_values.update({
    #         'api_url': payment_response['href'],
    #         'redirect_form_html': redirect_form_html,
    #     })
    #     return processing_values

    def _get_specific_rendering_values(self, processing_values):
        print('------------------------------------------------')
        print('Call come inside the rendering fn in paytrail')

        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'paytrail':
            print('not paytrail')
            return res

        print('Paytrail')

        endpoint = '/payments'
        payload = self._paytrail_prepare_payment_request_payload()
        print('-------------------------')
        print('come back to rendering fn')
        _logger.info("sending '/payments' request for link creation:\n%s", pprint.pformat(payload))
        payment_data = self.provider_id._paytrail_make_request(payload)
        print('--------------------------')
        print('Come back to rendering fn')

        # The provider reference is set now to allow fetching the payment status after redirection
        self.provider_reference = payment_data.get('id')

        # Extract the checkout URL from the payment data and add it with its query parameters to the
        # rendering values. Passing the query parameters separately is necessary to prevent them
        # from being stripped off when redirecting the user to the checkout URL, which can happen
        # when only one payment method is enabled on Mollie and query parameters are provided.
        checkout_url = payment_data['href']
        # parsed_url = urls.url_parse(checkout_url)
        # url_params = urls.url_decode(parsed_url.query)
        print('set all')
        return {'payment_url': checkout_url}
        # return print("RENDERING END")

    def _paytrail_prepare_payment_request_payload(self):
        """Generate payload for Paytrail payment request."""
        # ✅ Ensure correct currency conversion
        amount_in_cents = round(self.currency_id._convert(
            self.amount,
            self.env['res.currency'].search([("name", "=", "EUR")]),
            self.env.company,
            fields.Date.today()
        ) * 100)

        # ✅ Ensure amount is at least 1 cent
        if amount_in_cents < 1:
            _logger.error("Paytrail Error: Amount must be greater than 0. Current value: %s", amount_in_cents)
            raise ValidationError(_("Payment amount must be at least 0.01 EUR."))

        # ✅ Base URLs for redirection
        base_url = self.get_base_url()
        redirect_url = urls.url_join(base_url,'/payment/paytrail/return')

        # ✅ Ensure total amount matches items
        body = {
            "stamp": str(uuid.uuid4()),
            "reference": self.reference,
            "amount": int(amount_in_cents),  # Convert to integer
            "currency": "EUR",
            "language": "EN",
            "items": [
                {
                    "unitPrice": int(amount_in_cents),  # Ensure unitPrice matches total
                    "units": 1,  # Quantity
                    "vatPercentage": 0,
                    "productCode": "#1234",
                    "deliveryDate": str(fields.Date.today()),
                }
            ],
            "customer": {"email": self.partner_email},
            "redirectUrls": {"success": redirect_url, "cancel": redirect_url},
        }

        # ✅ Minimized JSON formatting
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
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'paytrail' or len(tx) == 1:
            return tx
        tx = self.search(
            [('reference', '=', notification_data.get('checkout-reference')), ('provider_code', '=', 'paytrail')]
        )
        if not tx:
            raise ValidationError("Paytrail: " + _(
                "No transaction found matching reference %s.", notification_data.get('checkout-reference')
            ))
        return tx

    def _process_notification_data(self, notification_data):
        """ Override of payment to process the transaction based on Mollie data.

        Note: self.ensure_one()

        :param dict notification_data: The notification data sent by the provider
        :return: None
        """
        super()._process_notification_data(notification_data)

        if self.provider_code != 'paytrail':
            return
        payment_status = notification_data.get('checkout-status')
        if payment_status in ['pending', 'delayed']:
            self._set_pending()
        elif payment_status == 'ok':
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