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
    var Dis = 0;

    for (var i = 0; i < currentOrder.length; i++) {
        const discount = this.discount;
        const discounted_amount = currentOrder[i].price_subtotal; // After discount
        const actual_price = currentOrder[i].price_unit * currentOrder[i].qty; // Original price
        const final_price = discounted_amount * currentOrder[i].qty; // Total after discount
        var individual_line_discount = actual_price - final_price; // Discount on this product
        var global_discount = 0;
        if(currentOrder[i].full_product_name === "Discount"){
            global_discount += Math.abs(discounted_amount);
        }
        Dis += individual_line_discount + global_discount; // Accumulate discount
    }

    console.log('Discount given for current order:', Dis);
    let add_to_session_balance = this.Total_discount_limit_balance + Dis
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
                title: _t("Discount Limit Exceed."),
                body: _t('The available balance for discount is Zero'),
            });
    }
    }
});


