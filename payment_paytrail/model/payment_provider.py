# -*- coding: utf-8 -*-
import hashlib
import hmac
import logging
import pprint
import uuid

import requests

from odoo import models, fields, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(
        selection_add=[("paytrail", "Paytrail")],
        ondelete={"paytrail": "set default"}
    )
    paytrail_merchant_id = fields.Char(string="Merchant Id")
    paytrail_secret_key = fields.Char(string="Secret Key")

    def _paytrail_make_request(self, body):
        """to make request into paytrail"""
        print(self.paytrail_merchant_id)
        print(self.paytrail_secret_key)
        paytrail_url = "https://services.paytrail.com/payments"
        secret = self.paytrail_secret_key
        headers = dict({
            "checkout-account": self.paytrail_merchant_id,
            "checkout-algorithm": "sha256",
            "checkout-method": "POST",
            "checkout-nonce": str(uuid.uuid4()),
            "checkout-timestamp": str(fields.Datetime.now().isoformat())
        })
        signature = self.calculate_hmac(secret, headers, body)
        headers["signature"] = signature

        try:
            print(paytrail_url)
            print(body)
            print(headers)
            response = requests.request(method="POST", url=paytrail_url, data=body, headers=headers,
                                        timeout=60)  # (data=body) will only work if its (json=body) then there will be signature mismatch cos paytrail expect encoded data if we give body as data it will encode that automatically.if its json it wont encode it will just pass
            if response.status_code == 201:
                _logger.info("payment successfully created")
            else:
                _logger.error("\nError:", response.text)
                print("\nError:", response.text)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                _logger.exception(
                    "Invalid API request at %s with data:\n%s", paytrail_url, pprint.pformat(body)
                )
                raise ValidationError(
                    "Paytrail: " + _(
                        "The communication with the API failed. Paytrail gave us the following "
                        "information: %s", response.json().get('detail', '')
                    ))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.exception("Unable to reach endpoint at %s", paytrail_url)
            raise ValidationError(
                "Paytrail: " + _("Could not establish the connection to the API.")
            )
        return response.json()

    def calculate_hmac(self, secret, headers, body):
        """to calculate hmac"""
        data = []
        for key, value in headers.items():
            if key.startswith('checkout-'):
                data.append('{key}:{value}'.format(key=key, value=value))
        data.append(body)
        hmac = self.compute_sha256_hash('\n'.join(data), secret)
        return hmac

    def compute_sha256_hash(self, message, secret):
        """to hash the hmac"""
        # whitespaces that were created during json parsing process must be removed
        hash = hmac.new(secret.encode(), message.encode(), digestmod=hashlib.sha256)
        return hash.hexdigest()

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

        if self.code == 'paytrail' and is_validation:
            return None
        return super()._get_redirect_form_view(is_validation)