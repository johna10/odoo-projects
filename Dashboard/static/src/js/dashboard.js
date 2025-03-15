/**@odoo-module **/
import { registry } from "@web/core/registry";
import { Component,useState } from  "@odoo/owl";
import { CustomDashboardComments } from "./dashboard_comments"
class CustomDashboard extends Component {
        setup(){
            console.log(this)
            this.state = useState({
                demo: 0,
                comment:''
            })
            this.num = 2
        }
        submitComment(){
            this.state.demo ++
            console.log(this.state.comment)
            const commentData = [{
            name: this.state.comment,
        }]
             this.env.services.orm.create('dashboard.comment', commentData)
        }
 }
CustomDashboard.components = {
    CustomDashboardComments,
};
CustomDashboard.template = "Dashboard.Custom_Dashboard";
//  Tag name that we entered in the first step.
registry.category("actions").add("custom_dashboard_tag", CustomDashboard);
