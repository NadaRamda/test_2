import xlsxwriter
import base64
import tempfile
from odoo import api, models, fields, _


class SaleOrderReportWizard(models.TransientModel):
    _name = 'sale.order.report.wizard'
    _description = 'sale.order.report.wizard'
    name = fields.Char(string="Report Name", required=True, default="sale orders")
    start_date = fields.Date(String="From", required=True)
    end_date = fields.Date(String="TO", required=True)
    filename = fields.Char(string='File Name', size=64)
    excel_file = fields.Binary(string='Report File')

    """pdf report"""
    def generate_report_pdf(self):
        data = {
            "start_date": self.start_date,
            "end_date": self.end_date
        }
        return self.env.ref('sale_order_report.report_pdf_wiz').report_action(self, data=data)


    """xlsx report"""
    def _get_data(self):
        domain = []
        start_date = self.start_date
        if start_date:
            domain += [('date_order', '>=', start_date)]
        end_date = self.end_date
        if end_date:
            domain += [('date_order', '<=', end_date)]
        orders = self.env['sale.order'].search(domain)
        data = {
            'orders': orders
        }
        return data

    def generate_report(self):
        self.ensure_one()
        data = self._get_data()
        temp_location = tempfile.mkstemp()[1]
        workbook = xlsxwriter.Workbook(temp_location + '.xlsx')
        title = workbook.add_format(
            {'bold': 'True', 'align': 'center', 'bg_color': '#e9ecef', 'border': True, 'font_size': 20, })
        format_table_header = workbook.add_format(
            {'bold': True, 'align': 'center', 'bg_color': '#e9ecef', 'border': True})
        data_format = workbook.add_format(
            {'align': 'center', 'border': 1, 'size': 12, 'num_format': '#,##0.00'})
        data_format2 = workbook.add_format(
            {'align': 'center', 'border': 1, 'size': 13, 'num_format': '#,##0.00'})
        """sheet 1"""
        sheet = workbook.add_worksheet('orders')
        row = 0
        col = 0
        sheet.set_column('A:A', 15)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:D', 15)
        sheet.set_column('E:E', 15)
        sheet.merge_range('A1:E2', 'Sale Orders', title)
        sheet.write('A4', 'From :', format_table_header)
        sheet.write('B4', self.start_date.strftime('%d/%B/%Y'), format_table_header)
        sheet.write('D4', 'TO :', format_table_header)
        sheet.write('E4', self.end_date.strftime('%d/%B/%Y'), format_table_header)
        col = 0
        row = 5
        # sheet.write(row, col, 'Number', format_table_header)
        # sheet.write(row, col + 1, 'Customer', format_table_header)
        # sheet.write(row, col + 2, 'Order Date', format_table_header)
        # sheet.write(row, col + 3, 'Status', format_table_header)
        # sheet.write(row, col + 4, 'Total', format_table_header)
        #
        # for obj in data['orders']:
        #     sheet.write(row+1, col, obj.name,data_format2)
        #     sheet.write(row+1, col + 1, obj.partner_id.name,data_format2)
        #     sheet.write(row+1, col + 2, obj.date_order.strftime('%d/%B/%Y'),data_format2)
        #     sheet.write(row+1, col + 3, obj.state,data_format2)
        #     sheet.write(row+1, col + 4, obj.amount_total,data_format2)
        #     row += 1
        #     sheet.merge_range(row + 1, col + 1, row + 1, col + 3, 'Lines', format_table_header)
        #     for x in obj.order_line:
        #         sheet.write(row +2, col, x.name,data_format)
        #         row += 1
        #     row += 1

        sheet.write(row, col, 'product', format_table_header)
        sheet.write(row, col + 1, 'Description', format_table_header)
        sheet.write(row, col + 2, 'Price', format_table_header)
        sheet.write(row, col + 3, 'Taxes', format_table_header)
        sheet.write(row, col + 4, 'total', format_table_header)
        for obj in data['orders']:
            sheet.merge_range(row + 1, col , row + 1, col + 1, 'Number : %s'%(obj.name), format_table_header)
            sheet.merge_range(row + 1, col + 3, row + 1, col + 4, 'Name : %s'%(obj.partner_id.name), format_table_header)
            for x in obj.order_line:
                sheet.write(row +2, col, x.product_id.name, data_format)
                sheet.write(row + 2, col+1, x.name, data_format)
                sheet.write(row + 2, col+2, x.product_uom_qty, data_format)
                sheet.write(row + 2, col+3, x.tax_id.name, data_format)
                sheet.write(row + 2, col+4, x.price_subtotal, data_format)

                row += 1
            row += 1
        workbook.close()
        fp = base64.encodestring(open(temp_location + '.xlsx', 'rb').read())
        file_name = 'saleorder_%s_to_%s.xlsx' % (self.start_date, self.end_date)
        self.write({'filename': 'file_name', 'excel_file': fp})
        return {
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=sale.order.report.wizard&field=excel_file&download=true&id=%s&filename=%s' % (
            self.id, file_name),
            'target': 'new',
        }




























# obj.pop('id')
            # obj.update({
            #     "date_order": obj.get('date_order').strftime('%d/%B/%Y'),
            #     "partner_id": obj.get('partner_id')[1],
            #     "user_id": obj.get('user_id')[1],
            # })
            # row += 1
            # total += obj['amount_total']
            # for col, key_in_obj in enumerate(obj):
            #     sheet.write(row, col, obj[key_in_obj])
# sheet.write(row + 1, col, total, format_table_header)
# sheet.write(row,col+5, 'total', format_table_header)
