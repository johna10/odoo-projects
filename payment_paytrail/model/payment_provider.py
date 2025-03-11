# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import uuid
import hmac
import hashlib
import json
from datetime import datetime, timezone

import requests
from werkzeug import urls

from odoo import _, fields, models, service
from odoo.exceptions import ValidationError

from odoo.addons.payment_mollie import const

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('paytrail', "Paytrail")], ondelete={'paytrail': 'set default'})
    paytrail_merchant_account = fields.Char(
        string="Merchant Account ID",
        help="The code of the merchant account to use with this provider"
        )
    paytrail_api_key = fields.Char(
        string="API Key", help="The API key of the webservice user")

    redirect_form_view_id = fields.Many2one(
        string="Redirect Form Template", comodel_name='ir.ui.view',
        help="The template rendering a form submitted to redirect the user when making a payment",
        domain=[('type', '=', 'qweb')],
        ondelete='restrict',
    )

    # === BUSINESS METHODS ===#

    def _get_supported_currencies(self):
        """ Override of `payment` to return the supported currencies. """
        supported_currencies = super()._get_supported_currencies()
        if self.code == 'mollie':
            supported_currencies = supported_currencies.filtered(
                lambda c: c.name in const.SUPPORTED_CURRENCIES
            )
        return supported_currencies

    def _paytrail_make_request(self, endpoint, data=None, method='POST'):
        print('--------------------------')
        print('Comes inside the payment API request')

        merchant_id = self.paytrail_merchant_account
        secret = self.paytrail_api_key
        self.ensure_one()

        #  Define required headers
        headers = {
            "checkout-method": method,
            "checkout-account": str(merchant_id),
            "checkout-algorithm": "sha256",
            "checkout-nonce": str(uuid.uuid4()),  # Unique nonce per request
            "checkout-timestamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds') + 'Z',
            "content-type": "application/json; charset=utf-8",
        }

        encData = self.calculate_hmac(secret, headers, data)

        print("Encrypted data: " + encData)
        headers["signature"] = encData
        print('Header----------------->',headers)
        #  Send the request
        endpoint = f'{endpoint.strip("/")}'
        url = urls.url_join('https://services.paytrail.com/', endpoint)

        print('Call Initiated')
        try:
            print(method)
            print(url)
            print(data)
            print(headers)

            response = requests.request("POST", url=url, data=data, headers=headers, timeout=60)
            response.raise_for_status()
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            _logger.exception("Error reaching Paytrail API: %s", url)
            raise ValidationError(_("Paytrail API request failed: %s") % str(e))

        return response.json()


    def calculate_hmac(self, secret, headerParams, body):
        data = []
        for key, value in headerParams.items():
            if key.startswith('checkout-'):
                data.append('{key}:{value}'.format(key=key, value=value))

        data.append(body)
        return self.compute_sha256_hash('\n'.join(data), secret)

    def compute_sha256_hash(self, message, secret):
        # whitespaces that were created during json parsing process must be removed
        hash = hmac.new(secret.encode(), message.encode(), digestmod=hashlib.sha256)
        return hash.hexdigest()









