import { cookie } from "@web/core/browser/cookie";
import publicWidget from '@web/legacy/js/public/public_widget';
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";
export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}

function _generateUniqueId() {
  return Date.now() + Math.random().toString(36).substr(2);;
}

var SchoolWebsiteEvents = publicWidget.Widget.extend({
        selector: '.school_website_event_snippet',
        willStart: async function () {
            const data = await rpc('/school/events/', {})
            const events = data
            const unique_id = _generateUniqueId()
            Object.assign(this, {
                events,
                unique_id
            })
        },
        start: function () {
            const refEl = this.$el.find("#latest_school_events")
            var chunks = _chunk(this.events, 4)
            chunks[0].is_active = true
            var carousal_unique_id = this.unique_id
            refEl.html(renderToElement('school.school_latest_events',{
            chunks,
            carousal_unique_id
            }))
        }
    });
publicWidget.registry.SchoolWebsiteEvents = SchoolWebsiteEvents;
return SchoolWebsiteEvents;





