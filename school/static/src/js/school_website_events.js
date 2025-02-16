import { cookie } from "@web/core/browser/cookie";
import publicWidget from '@web/legacy/js/public/public_widget';
import { rpc } from "@web/core/network/rpc";


publicWidget.registry.WebsiteCustomerContactRequestForm = publicWidget.Widget.extend({
   selector: "#wrap",
   events: {
     "change #aadhaar_number": "_onEmailAadhaarChange"
   },
     _onEmailAadhaarChange: async function (ev) {
     rpc('/email/aadhaar/rpc/check', {email:this.$el.find('#email').val(), aadhar:this.$el.find('#aadhaar_number').val()}).then((res)=>{
                if(res.email_taken){
                    alert('This email is already Taken.')
                }
                if(res.aadhar_taken){
                    alert('This Aadhaar Number is already Taken.')
                }
       })
     }
})

