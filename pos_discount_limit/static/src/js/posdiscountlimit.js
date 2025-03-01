import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { patch } from "@web/core/utils/patch";

console.log('hai')
patch(PosStore.prototype, {
    async pay(){
    const currentOrder = this.get_order().get_orderlines();
    console.log('Current Orders', currentOrder)
    console.log('Current Orders length', currentOrder.length)

    var Total_discount_limit_balance = this.config.discount_fixed_limit
    console.log('Limit ', Total_discount_limit_balance);
    console.log('--------------------------------------------------------------------------------');

    var Dis = 0;
    for (var i = 0; i < currentOrder.length; i++) {
        const discount = this.discount; // Ensure this is correctly assigned
        const discounted_amount = currentOrder[i].price_subtotal; // After discount
        const actual_price = currentOrder[i].price_unit * currentOrder[i].qty; // Original price
        const final_price = discounted_amount * currentOrder[i].qty; // Total after discount
        var individual_line_discount = actual_price - final_price; // Discount on this product

        Dis += individual_line_discount; // Accumulate discount

        console.log(currentOrder[i].full_product_name);
        console.log('Discount', discount);
        console.log('After Discount', discounted_amount);
        console.log('Final Price', final_price);
        console.log('Actual Price', actual_price);
    }
    console.log('--------------------------------------------------------------------------------');
    console.log('Total Discount Taken:', Dis);
    Total_discount_limit_balance = Total_discount_limit_balance - Dis
    console.log('Discount Balance :', Total_discount_limit_balance);

    if(Total_discount_limit_balance > 0){
        console.log('Balance present');
        alert('have Balance ');
        return super.pay();
    }
    else{
        console.log('No Balance');
        alert('No Balance');
    }
    }
});

