import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";


patch(PosStore.prototype, {
    async processServerData(){
        super.processServerData();
        this.total_discount_limit_balance = this.config.current_session_id.session_discount_balance
    },

    async pay(){
        this.discount_limit_of_session = this.config.discount_fixed_limit;
        const currentOrder = this.get_order().get_orderlines();
        var global_discount = 0;
        var individual_line_discount = 0;
        var Dis = 0;
        for (var i = 0; i < currentOrder.length; i++) {
            let product = currentOrder[i];
            if (product.full_product_name === "Discount" && product.qty != 0) {
                let discounted_amount = product.price_subtotal;
                global_discount += Math.abs(discounted_amount);
            }
            else{
                let product_discount = 0;
                if (product.discount) {
                    let discounted_amount = product.price_subtotal; // Price After discount
                    let actual_price = product.price_unit * product.qty; // Original price without discount
                    let discount_applied = actual_price - discounted_amount; // Discount given for this product
                    if (discount_applied > 0) {
                        product_discount = discount_applied; // Store discount only for this product
                    }
                }
                individual_line_discount += product_discount; // Accumulate only the current product's discount
            }
        }
        Dis = individual_line_discount + global_discount;
        this.total_discount_limit_balance = this.total_discount_limit_balance || 0;
        var add_to_session_balance = this.total_discount_limit_balance + Dis
        if( 0 <= add_to_session_balance && add_to_session_balance < this.discount_limit_of_session){
            this.total_discount_limit_balance = add_to_session_balance;
            await this.env.services.orm.call(
                    "pos.session",
                    "sample",
                    [
                    this.config.current_session_id.id,
                    this.total_discount_limit_balance,
                    ]);

            return await super.pay();
        }
        else{
            this.dialog.add(AlertDialog, {
                    title: _t("Discount Limit Exceed."),
                    body: _t('Discount limit for the current session is over. Please remove the discount to continue.'),
                                         });
        }
    }
});


