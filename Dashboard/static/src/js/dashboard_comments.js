/**@odoo-module **/
import { registry } from "@web/core/registry";
import { Component,useState } from  "@odoo/owl";
export class CustomDashboardComments extends Component {
    setup(){
        console.log(this,'child')
    }


 }
CustomDashboardComments.template = "Dashboard.Custom_Dashboard_comment";
