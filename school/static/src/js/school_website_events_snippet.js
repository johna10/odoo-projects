import { cookie } from "@web/core/browser/cookie";
import publicWidget from '@web/legacy/js/public/public_widget';
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";

console.log('events start')

var SchoolWebsiteEvents = publicWidget.Widget.extend({
        selector: '.school_website_event_snippet',

        willStart: async function () {
            console.log('inside willstart')
            const data = await rpc('/school/events/', {})
            console.log('data -',data)

            const events = data
            Object.assign(this, {
                events
            })
            console.log('wiil start end')
        },
        start: function () {
            console.log('start start')
            const refEl = this.$el.find("#top_products_carousel")

            const all_events = this.events
            console.log(all_events)

            refEl.html(renderToElement('school.products_category_wise',{
            all_events,
            }))
            console.log('start end')
        }
    });


publicWidget.registry.SchoolWebsiteEvents = SchoolWebsiteEvents;
console.log('event end')
return SchoolWebsiteEvents;





