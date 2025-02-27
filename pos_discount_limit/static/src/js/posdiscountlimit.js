import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

console.log('hai')

patch(PosOrderline.prototype, {

    setup(vals) {
        this.brand_id = this.product_id.brand_id || "";
        return super.setup(...arguments);
    },

    getDisplayData() {
    console.log('this ->' , this)
    console.log('this -> discount type ', this.config.discount_type)
    console.log('this -> fixed discount limit' , this.config.discount_fixed_limit)
    console.log('this -> percentage discount limit' , this.config.discount_percentage_limit)
    console.log('this -> line discount' , this.discount)
    console.log('this -> global discount')
    console.log('-----------------------------------------------------------------------------')

    if(this.config.discount_type == 'fixed'){
        console.log('Type is Fixed')
    }
    else if(this.config.discount_type == 'percentage'){
        console.log('Type is Percentage')
        const limited_discount = this.config.discount_percentage_limit
        const applied_discount = this.discount
        if(limited_discount < applied_discount){
            console.log('Limit')
              alert('Discount Cross the Limit');
        }
        else{
            console.log('No Limit')
        }
    }
    else{
        console.log('Nothing')
    }

        return {
            ...super.getDisplayData(),
            brand: this.brand_id.name || "",
        };
    },
});






















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
