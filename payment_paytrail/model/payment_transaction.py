# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import json
from werkzeug import urls
import uuid

from odoo import _, models, fields
_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

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
        payment_data = self.provider_id._paytrail_make_request(endpoint, data=payload)
        print('--------------------------')
        print('Come back to rendering fn')

        # The provider reference is set now to allow fetching the payment status after redirection
        self.provider_reference = payment_data.get('id')

        # Extract the checkout URL from the payment data and add it with its query parameters to the
        # rendering values. Passing the query parameters separately is necessary to prevent them
        # from being stripped off when redirecting the user to the checkout URL, which can happen
        # when only one payment method is enabled on Mollie and query parameters are provided.
        # checkout_url = payment_data['_links']['checkout']['href']
        # parsed_url = urls.url_parse(checkout_url)
        # url_params = urls.url_decode(parsed_url.query)
        print('set all')
        # return {'api_url': checkout_url, 'url_params': url_params}
        return print("RENDERING END")

    def _paytrail_prepare_payment_request_payload(self):
        print('------------------------')
        print('Comes to Payload fn')
        """ Create the payload for the payment request based on the transaction values.

        :return: The request payload
        :rtype: dict
        """
        amount_in_euro = self.amount * self.env['res.currency'].search([("name", "=", "EUR")]).rate
        base_url = 'https://def4-103-139-64-225.ngrok-free.app/'
        redirect_url = urls.url_join(base_url, '/payment/paytrail/return')

        body = dict({
            "stamp": str(uuid.uuid4()),
            "reference": self.reference,
            "amount": int(amount_in_euro * 100),
            "currency": "EUR",
            "language": 'EN',
            "items": [{"unitPrice": int(amount_in_euro * 100), "units": 1, "varPercentage": 0, "productCode": "#1234",
                       "deliveryDate": str(fields.Date.today())}],
            "customer": {"email": self.partner_email},
            "redirectUrls": {"success": redirect_url, "cancel": redirect_url}
        })
        payload = json.dumps(body, separators=(',', ':'))
        print(payload)
        print('return payload')
        return payload

