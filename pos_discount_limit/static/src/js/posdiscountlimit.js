import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { patch } from "@web/core/utils/patch";

console.log('hai')
//console.log(this)
patch(PosStore.prototype, {
    async pay(){
    console.log('CLICKED')
    console.log('this ->' , this)

    console.log('this -> discount type ', this.config.discount_type)
    console.log('this -> discount type ', this.config.discount_type)
    console.log('this -> fixed discount limit' , this.config.discount_fixed_limit)
    console.log('this -> percentage discount limit' , this.config.discount_percentage_limit)
    console.log('this -> line discount' , this.discount)
    console.log('this -> global discount')
    console.log('-----------------------------------------------------------------------------')

    const currentOrder = this.get_order().get_orderlines();
    console.log('Current Orders', currentOrder)
    console.log('Current Orders length', currentOrder.length)

    const Total_discount_limit_balance = this.config.discount_fixed_limit

    for (var i = 0; i < currentOrder.length; i++) {

         const discount =  this.discount
         const discounted_amount = currentOrder[i].price_subtotal
         const final_price = currentOrder[i].price_subtotal * currentOrder[i].qty
         actual_price = currentOrder[i].price_unit * currentOrder[i].qty
         discount_taken = actual_price - final_price

         console.log(currentOrder[i].full_product_name)
         console.log('Discount', discount)
         console.log('Discounted Amount', discounted_amount)
         console.log('final Price', final_price)
         console.log('Actual Price', actual_price )
         console.log('Discount taken', discount_taken )


        }
    }
});


//patch(PosOrderline.prototype, {
//
//    setup(vals) {
//        this.brand_id = this.product_id.brand_id || "";
//        return super.setup(...arguments);
//    },
//
//    getDisplayData() {
//    console.log('this ->' , this)
//
//    if(this.config.discount_type == 'fixed'){
//        console.log('Type is Fixed')
//        const per_session_limit_amount = this.config.discount_fixed_limit
//        console.log('Fixed Amount', per_session_limit_amount - 1)
//        console.log('Unit price', this.price_unit)
//        const currentOrder = this.get_order();
//        console.log('Current Orders', currentOrder)
//
//
//
//
//    }
//    else if(this.config.discount_type == 'percentage'){
//        console.log('Type is Percentage')
//        const limited_discount = this.config.discount_percentage_limit
//        const applied_discount = this.discount
//        if(limited_discount < applied_discount){
//            console.log('Limit')
//            alert('Discount Cross the Limit');
//        }
//        else{
//            console.log('No Limit')
//        }
//    }
//    else{
//        console.log('Nothing')
//    }
//
//        return {
//            ...super.getDisplayData(),
//            brand: this.brand_id.name || "",
//        };
//    },
//});






















//console.log(pos.config.discount_fixed_limit)
//console.log(pos.config.discount_percentage_limit)

//import { Component } from "@odoo/owl";
//import { usePos } from "@point_of_sale/app/store/pos_store";
//
//export class MyDiscountComponent extends Component {
//    setup() {
//        this.pos = usePos(); // Access POS store
//    }
//
//    get discountLimitEnabled() {
//        return this.pos.config.is_discount_limit; // Access your custom field
//    }
//
//    get discountType() {
//        return this.pos.config.discount_type;
//    }
//}
//
//const pos = odoo.__DEBUG__.services['pos'].pos;
//
//function applyDiscount(order, discountValue) {
//    if (pos.config.is_discount_limit) {
//        if (pos.config.discount_type === "fixed") {
//            if (discountValue > pos.config.discount_fixed_limit) {
//                console.log("Discount exceeds fixed limit!");
//                return false;
//            }
//        } else if (pos.config.discount_type === "percentage") {
//            if (discountValue > pos.config.discount_percentage_limit) {
//                console.log("Discount exceeds percentage limit!");
//                return false;
//            }
//        }
//    }
//
//    // Apply the discount if within limit
//    order.set_discount(discountValue);
//    return true;
//}
