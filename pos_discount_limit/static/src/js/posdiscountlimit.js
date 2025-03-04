import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

console.log(this.config)
console.log('hai')
patch(PosStore.prototype, {
    async processServerData(){
        super.processServerData();
        this.Total_discount_limit_balance = this.config.current_session_id.session_discount_balance
        console.log('Present Session given Discount', this.Total_discount_limit_balance);
        console.log('###################################');
    },

    async pay(){

        console.log('Current Opened Session ID :',this.config.current_session_id.id)

        this.discount_limit_of_session = this.config.discount_fixed_limit;
        console.log("Limit given to current Shop :", this.discount_limit_of_session)

        const currentOrder = this.get_order().get_orderlines();

        console.log('Length of the order line:', currentOrder.length);

        var global_discount = 0;
        var individual_line_discount = 0;
        var Dis = 0;

        for (var i = 0; i < currentOrder.length; i++) {
            let product = currentOrder[i];

            if (product.full_product_name === "Discount") {
                console.log("DISCOUNT PRODUCT");
                let discounted_amount = product.price_subtotal;
                console.log("Discount product price:", discounted_amount);
                global_discount += Math.abs(discounted_amount);
            } else {
                console.log('--------------------');
                console.log(product.full_product_name);
                console.log('Discount given :',product.discount);
                let product_discount = 0; // Store discount for the current product

                if (product.discount) {
                    console.log("Product has discount");
                    let discounted_amount = product.price_subtotal; // After discount
                    let actual_price = product.price_unit * product.qty; // Original price without discount
                    let discount_applied = actual_price - discounted_amount; // Discount for this product

                    console.log("Product price after discount applied:", discounted_amount);
                    console.log("Product actual price:", actual_price);
                    console.log("Discount applied:", discount_applied);

                    if (discount_applied > 0) {
                        console.log("Discount is applied");
                        product_discount = discount_applied; // Store discount only for this product
                    } else {
                        console.log("Discount is not applied");
                    }
                } else {
                    console.log("Product has no line-wise discount");
                }

                individual_line_discount += product_discount; // Accumulate only the current product's discount
                console.log("Sum of individual line discounts:", individual_line_discount);
                console.log("---------------------");
            }
        }

        // **Move the total discount calculation outside the loop**
        Dis = individual_line_discount + global_discount;
        console.log("Final Discount given for current order:", Dis);

        this.Total_discount_limit_balance = this.Total_discount_limit_balance || 0;
        var add_to_session_balance = this.Total_discount_limit_balance + Dis
        console.log('Total Discount given by the session :', add_to_session_balance);

        if( 0 <= add_to_session_balance && add_to_session_balance < this.discount_limit_of_session){
            console.log('Balance present');
            this.Total_discount_limit_balance = add_to_session_balance;
            console.log('Updated Balance from local', this.Total_discount_limit_balance)

           await this.env.services.orm.call(
                    "pos.session",
                    "sample",
                    [
                    this.config.current_session_id.id,
                    this.Total_discount_limit_balance,
                    ]);

            return await super.pay();
        }
        else{
            console.log('No Balance');
            this.dialog.add(AlertDialog, {
                    title: _t("Discount Limit Exceed.                                                "),
                    body: _t('Discount limit for the current session is over. Please remove the discount to continue.'),
                });
        }
    }
});


