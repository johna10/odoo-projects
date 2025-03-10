# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint

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
        print('---------------------------')
        print('Call Comes inside Request CALL')
        print('endpoint----->', endpoint)
        print('Data----->', endpoint)
        """ Make a request at mollie endpoint.

        Note: self.ensure_one()

        :param str endpoint: The endpoint to be reached by the request
        :param dict data: The payload of the request
        :param str method: The HTTP method of the request
        :return The JSON-formatted content of the response
        :rtype: dict
        :raise: ValidationError if an HTTP error occurs
        """
        self.ensure_one()
        endpoint = f'/v2/{endpoint.strip("/")}'
        url = urls.url_join('https://api.paytrail.com/', endpoint)

        odoo_version = service.common.exp_version()['server_version']
        module_version = self.env.ref('base.module_payment_mollie').installed_version
        print("HEADER SETTING")
        headers = {
            "Accept": "application/json",
            "Authorization": f'Bearer {self.paytrail_api_key}',
            "Content-Type": "application/json",
            # See https://docs.mollie.com/integration-partners/user-agent-strings
            "User-Agent": f'Odoo/{odoo_version} MollieNativeOdoo/{module_version}',
        }
        print("HEADER SET")

        try:
            print('API')
            response = requests.request(method, url, json=data, headers=headers, timeout=60)
            print('API CALLED')
            # try:
            #     response.raise_for_status()
            # except requests.exceptions.HTTPError:
            #     _logger.exception(
            #         "Invalid API request at %s with data:\n%s", url, pprint.pformat(data)
            #     )
            #     raise ValidationError(
            #         "Mollie: " + _(
            #             "The communication with the API failed. Mollie gave us the following "
            #             "information: %s", response.json().get('detail', '')
            #         ))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.exception("Unable to reach endpoint at %s", url)
            raise ValidationError(
                "Mollie: " + _("Could not establish the connection to the API.")
            )
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
