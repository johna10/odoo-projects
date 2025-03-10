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
        """Make a request to the Paytrail API with a properly signed header.

        :param str endpoint: The Paytrail API endpoint (without base URL)
        :param dict data: Request body (if any)
        :param str method: HTTP method ('POST' or 'GET')
        :return: JSON response from Paytrail
        :rtype: dict
        :raise: ValidationError if an HTTP error occurs
        """
        self.ensure_one()

        # ✅ Step 1: Define required headers
        headers = {
            "checkout-method": method,
            "checkout-account": str(self.paytrail_merchant_account),
            "checkout-algorithm": "sha256",
            "checkout-nonce": str(uuid.uuid4()),  # Unique nonce per request
            "checkout-timestamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds') + 'Z',
            "content-type": "application/json; charset=utf-8"
        }
        print("Header set")
        print(headers)

        # ✅ Step 2: Sort headers alphabetically
        sorted_headers = dict(sorted(headers.items()))
        print('sorted headers')
        print(sorted_headers)

        # ✅ Step 3: Create the signature payload
        def generate_signature_payload(headers, body=None):
            """Format headers and body into a signature payload."""
            payload = "\n".join(f"{key}:{value}" for key, value in headers.items())

            # Ensure the body is handled properly
            if body:
                json_body = json.dumps(body, separators=(',', ':'))  # Minimized JSON format
            else:
                json_body = ""  # Paytrail requires a newline even if body is empty

            return payload + "\n" + json_body  # Ensure newline before the body

        signature_payload = generate_signature_payload(sorted_headers, data)

        print('signature payload is created')
        print(signature_payload)

        # ✅ Step 4: Generate HMAC-SHA256 signature
        def generate_signature(payload, secret_key):
            """Create HMAC SHA-256 signature."""
            return hmac.new(secret_key.encode(), payload.encode(), hashlib.sha256).hexdigest()

        print('ID:',self.paytrail_merchant_account)
        print('KEY :',self.paytrail_api_key)
        signature = generate_signature(signature_payload, self.paytrail_api_key)

        print('Signature is created')
        print(signature)

        # ✅ Step 5: Append signature to headers
        sorted_headers["signature"] = signature
        print('Signature appended')
        print(sorted_headers)


        print('BEFORE ENDPOINT STRIPED:', endpoint)
        # ✅ Step 6: Send the request
        endpoint = f'/v2/{endpoint.strip("/")}'
        print("AFTER ENDPOINT STRIPED:", endpoint)
        url = urls.url_join('https://services.paytrail.com/', endpoint)

        print('Call Initiated')
        try:
            response = requests.request(method, url, json=data, headers=sorted_headers, timeout=60)
            response.raise_for_status()
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            _logger.exception("Error reaching Paytrail API: %s", url)
            raise ValidationError(_("Paytrail API request failed: %s") % str(e))

        return response.json()

    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'paytrail':
            return default_codes
        return const.DEFAULT_PAYMENT_METHOD_CODES

# === BUSINESS METHODS - GETTERS === #

    def _get_redirect_form_view(self, is_validation=False):
        """ Override of `payment` to avoid rendering the form view for validation operations.

        Unlike other compatible payment methods in Xendit, `Card` is implemented using a direct
        flow. To avoid rendering a useless template, and also to avoid computing wrong values, this
        method returns `None` for Xendit's validation operations (Card is and will always be the
        sole tokenizable payment method for Xendit).

        Note: `self.ensure_one()`

        :param bool is_validation: Whether the operation is a validation.
        :return: The view of the redirect form template or None.
        :rtype: ir.ui.view | None
        """
        self.ensure_one()

        if self.code == 'xendit' and is_validation:
            return None
        return super()._get_redirect_form_view(is_validation)
