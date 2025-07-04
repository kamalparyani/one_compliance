import frappe
from frappe.model.mapper import *
from frappe import _
from frappe.utils import getdate, today, get_link_to_form


@frappe.whitelist()
def make_engagement_letter(source_name,target_name=None):

    doclist = get_mapped_doc(
        "Opportunity",
        source_name,
        {
            "Opportunity": {
                "doctype": "Engagement Letter",
                "field_map": {"name": "engagement_letter","engagement_letter_type":"Preliminary analysis & report"},

            }
        },
        target_name
    )


    return doclist

@frappe.whitelist()
def create_event_from_opportunity(oppotunity,event_category,start_on,subject,attendees):
    attendees = json.loads(attendees)
    event = frappe.new_doc('Event')
    event.event_category = event_category
    event.subject = subject
    event.starts_on = start_on
    event.append('event_participants', {
        'reference_doctype': 'Opportunity',
        'reference_docname': oppotunity
    })
    for attendee in attendees:
        event.append('event_participants', {
            'reference_doctype': attendee.get('attendee_type'),
            'reference_docname': attendee.get('attendee')
        })
    event.insert(ignore_permissions = True)
    return event.name






# @frappe.whitelist()
# def create_sales_order(opportunity):
#     '''
#         This method will create a Customer if not exists,
#         Then create a Service Order against that customer from Opportunity
#     '''
#     if frappe.db.exists('Opportunity', opportunity):
#         opportunity_doc = frappe.get_doc('Opportunity', opportunity)
#         customer = create_if_customer_not_exists(opportunity)
#         sales_order_doc = frappe.new_doc('Sales Order')
#         sales_order_doc.customer = customer
#         sales_order_doc.transaction_date = getdate(today())
#         sales_order_doc.delivery_date = getdate(today())
#         sales_order_doc.custom_create_project_automatically = frappe.db.get_single_value('Compliance Settings', 'create_project_from_sales_order_automatically')
#         if opportunity_doc.items:
#             #Adding Service Items from Opportunity
#             for item in opportunity_doc.items:
#                 sales_order_doc.append('items',{
#                     'item_code': item.item_code,
#                     'item_name': item.item_name,
#                     'uom': item.uom,
#                     'qty': item.qty,
#                     'rate': item.rate
#                 })
#         sales_order_doc.flags.ignore_mandatory = True
#         sales_order_doc.save(ignore_permissions=True)
#         opportunity_doc.status = 'Converted'
#         opportunity_doc.save()
#         frappe.msgprint('Sales Order {0} Created.'.format(get_link_to_form('Sales Order', sales_order_doc.name)), alert=True, indicator='green')

# def create_if_customer_not_exists(opportunity):
#     '''
#         This method will return Customer Id of given Opportunity
#         Also create a customer if not exists
#     '''
#     opportunity_from, party_name = frappe.db.get_value('Opportunity', opportunity, ['opportunity_from', 'party_name'])
#     if opportunity_from == 'Customer':
#         return party_name
#     if frappe.db.exists('Customer', { 'opportunity_name':opportunity }):
#         customer_id = frappe.db.get_value('Customer', { 'opportunity_name':opportunity })
#     else:
#         opportunity_detail = frappe.db.get_value('Opportunity', opportunity, ['contact_person', 'custom_customer_type'], as_dict=True)
#         default_customer_type = frappe.db.get_single_value('Compliance Settings', 'customer_type')
#         customer_doc = frappe.new_doc('Customer')
#         customer_doc.opportunity_name = opportunity
#         customer_doc.customer_name = opportunity_detail.get('contact_person') or ''
#         if opportunity_detail.get('custom_customer_type'):
#             customer_doc.compliance_customer_type = opportunity_detail.get('custom_customer_type')
#         elif default_customer_type:
#             customer_doc.compliance_customer_type = default_customer_type
#         customer_doc.flags.ignore_mandatory = True
#         customer_doc.save(ignore_permissions=True)
#         customer_id = customer_doc.name
#     return customer_id




@frappe.whitelist()
def create_sales_order(opportunity):
    if not frappe.db.exists('Opportunity', opportunity):
        frappe.throw("Opportunity not found")

    opp = frappe.get_doc('Opportunity', opportunity)
    customer = create_if_customer_not_exists(opp)

    items = []
    for i in opp.items:
        items.append({
            "item_code": i.item_code,
            "item_name": i.item_name,
            "uom": i.uom,
            "qty": i.qty,
            "rate": i.rate
        })

    return {
        "customer": customer,
        "items": items
    }

def create_if_customer_not_exists(opp):
    if opp.opportunity_from == 'Customer':
        return opp.party_name

    existing = frappe.db.get_value('Customer', {'opportunity_name': opp.name})
    if existing:
        return existing

    customer = frappe.new_doc('Customer')
    customer.opportunity_name = opp.name
    customer.customer_name = opp.contact_person or "Unnamed Customer"
    customer.compliance_customer_type = opp.custom_customer_type or frappe.db.get_single_value("Compliance Settings", "customer_type")
    customer.flags.ignore_mandatory = True
    customer.save(ignore_permissions=True)
    return customer.name
