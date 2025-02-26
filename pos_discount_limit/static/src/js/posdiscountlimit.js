console.log('hai')
console.log('this -> ' , this)

import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_store";

export class MyDiscountComponent extends Component {
    setup() {
        this.pos = usePos(); // Access POS store
    }

    get discountLimitEnabled() {
        return this.pos.config.is_discount_limit; // Access your custom field
    }

    get discountType() {
        return this.pos.config.discount_type;
    }
}

const pos = odoo.__DEBUG__.services['pos'].pos;

function applyDiscount(order, discountValue) {
    if (pos.config.is_discount_limit) {
        if (pos.config.discount_type === "fixed") {
            if (discountValue > pos.config.discount_fixed_limit) {
                console.log("Discount exceeds fixed limit!");
                return false;
            }
        } else if (pos.config.discount_type === "percentage") {
            if (discountValue > pos.config.discount_percentage_limit) {
                console.log("Discount exceeds percentage limit!");
                return false;
            }
        }
    }

    // Apply the discount if within limit
    order.set_discount(discountValue);
    return true;
}
