import { cookie } from "@web/core/browser/cookie";
import publicWidget from '@web/legacy/js/public/public_widget';
import { rpc } from "@web/core/network/rpc";

console.log('Student start')

publicWidget.registry.WebsiteCustomerContactRequestForm = publicWidget.Widget.extend({
   selector: "#wrap",
   events: {
     "change #date_of_birth": "_onDobChange",
     "change #email": "_onEmailAadhaarChange",
     "change #aadhaar_number": "_onEmailAadhaarChange"
   },

     _onDobChange: function (ev) {
     var date_from_from = this.$el.find('#date_of_birth').val();
     var today = new Date();
     var date = new Date(date_from_from)
     var dayDiff = Math.round(today - date) / (1000 * 60 * 60 * 24 * 365);
     $('#age').val(parseInt(dayDiff))
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

console.log('Student end')
console.log('--------------------------------------------------------------------------------------------------------------')


