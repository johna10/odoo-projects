import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";


patch(PosOrderline.prototype, {
    setup(vals) {
        this.brand_id = this.product_id.brand_id || "";
        return super.setup(...arguments);
    },
    getDisplayData() {
        return {
            ...super.getDisplayData(),
            brand: this.brand_id.name || "",
        };
    },
});

patch(Orderline, {
    props: {
        ...Orderline.props,
        line: {
            ...Orderline.props.line,
            shape: {
                ...Orderline.props.line.shape,
                brand: { type: String, optional: true },
            },
        },
    },
});




