from odoo import models, fields, api,_
class ReportPdf(models.AbstractModel):
    _name = 'report.sale_order_report.report_pdf_sale_orders'
    _description = 'sale_order_report'
    @api.model
    def _get_report_values(self, docids, data=None):
        domain = []
        start_date = data['start_date']
        if start_date:
            domain += [('date_order', '>=', start_date)]
        end_date = data['end_date']
        if end_date:
            domain += [('date_order', '<=', end_date)]
        orders = self.env['sale.order'].search(domain)
        print("orders", orders)
        print("data", data)
        return {
            'orders': orders,
            "data": data,
        }

















# class ReportPdfButton(models.AbstractModel):
#     _name = 'report.company.report_sale_orders'
#     _description = 'company Reports'
#
#     @api.model
#     def _get_report_values(self, docids, data=None):
#         docs = self.env['sale.order'].search([])
#         return {
#             "docs": docs,
#         }
