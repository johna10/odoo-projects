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


        console.log('Length of the order line ',currentOrder.length )









        var Dis = 0;
        var global_discount = 0;
        var individual_line_discount = 0;

        for (var i = 0; i < currentOrder.length; i++) {

              if(currentOrder[i].full_product_name === "Discount"){
                    console.log("DISCOUNT PRODUCT")
                    var discounted_amount = currentOrder[i].price_subtotal;
                    console.log('Discount product price',discounted_amount)
                    global_discount += Math.abs(discounted_amount);
              }
              else{
                    console.log(currentOrder[i].discount)
                    if(currentOrder[i].discount){
                        console.log('Product have discount ')
                        var discounted_amount = currentOrder[i].price_subtotal; // After discount
                        var actual_price = currentOrder[i].price_unit * currentOrder[i].qty; // Original price without discount
                        var final_price = discounted_amount// Total after discount

                            console.log(' product price after discount applied',discounted_amount)
                            console.log(' product actual price ',actual_price)
                            console.log(' product final price',final_price)

                        if(discounted_amount != actual_price){
                            console.log('Discount is applied')
                            individual_line_discount += actual_price - final_price; // Discount on this product
                        }
                        else{
                            console.log('Discount is not applied')
                        }
                    }
                    else{
                            console.log('Product have no discount')
                    }
                      console.log(' product individual line discount',individual_line_discount)
                      console.log('---------------------')
              }







//            if(currentOrder[i].full_product_name === "Discount"){
//                console.log("DISCOUNT PRODUCT")
//                var discounted_amount = currentOrder[i].price_subtotal;
//                console.log('Discount product price',discounted_amount)
//                global_discount += Math.abs(discounted_amount);
//            }
//            else{
//                console.log('NON DISCOUNT PRODUCT')
//                var discounted_amount = currentOrder[i].price_subtotal; // After discount
//                var actual_price = currentOrder[i].price_unit * currentOrder[i].qty; // Original price without discount
//                var final_price = discounted_amount// Total after discount
//
//                console.log(' product price after discount applied',discounted_amount)
//                console.log(' product actual price ',actual_price)
//                console.log(' product final price',final_price)
//
//                if(discounted_amount != actual_price){
//                    console.log('Discount is applied')
//                    individual_line_discount = actual_price - final_price; // Discount on this product
//                }
//                else{
//                    console.log('Discount is not applied')
//                }
//                console.log(' product individual line discount',individual_line_discount)
//
//            }
//            Dis += individual_line_discount + global_discount; // Accumulate discount
//            console.log('/////////////////////////')
        }














        console.log('Discount given for current order:', Dis);
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
                    title: _t("Discount Limit Exceed."),
                    body: _t('The available balance for discount is Zero'),
                });
        }
    }
});


