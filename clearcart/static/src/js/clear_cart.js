import { cookie } from "@web/core/browser/cookie";
import publicWidget from '@web/legacy/js/public/public_widget';
import { rpc } from "@web/core/network/rpc";


if($('.o_cart_product').length < 1){
      $('#clear_cart_button').hide();
                  }
publicWidget.registry.WebsiteSaleCartAllClear = publicWidget.Widget.extend({
    selector: '.oe_website_sale',
    events: {
        'click #clear_cart_button': '_onClickDeleteAllProduct',
    },
    _onClickDeleteAllProduct: function (ev) {
        rpc("/shop/cart/clear", {}).then(function(){
                location.reload();
            });
    },
});