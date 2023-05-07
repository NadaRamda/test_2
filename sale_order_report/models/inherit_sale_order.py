import json
import requests
from odoo import models, fields, api, _

headers = {'content-type': 'application/json', 'Accept': 'application/json', 'Authorization': 'nada'}

class ResConfigSetting(models.TransientModel):
    _inherit = ['res.config.settings']

    acsses = fields.Char(string='Delay alert contract outdated', config_parameter='sale_order_report.acsses')
    @api.model
    def set_values(self):
        res = super(ResConfigSetting, self).get_values()
        self.env['ir.config_parameter'].sudo().get_param('sale_order_report.acsses', self.acsses)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSetting, self).get_values()
        token = self.env['ir.config_parameter'].sudo().get_param('sale_order_report.acsses',)
        if token:
            res.update(
                acsses=token
            )
        return res

class InheritSale(models.Model):
    _inherit = ['sale.order']
    def action_confirm(self):
        print("Hi")
        res = super(InheritSale, self).action_confirm()
        url = 'http://0.0.0.0:8015/api/post/createsaleorder'
        list = []
        for line in self.order_line:
            list.append({"Product_id": line.product_id.id,
                         "Price_unit": line.price_unit,
                         "Description": line.name,
                         "Qty": line.product_uom_qty})
        data = {"CustomerCodeID": self.id,
                "CustomerName": self.display_name,
                "Lines": list, }
        data = json.dumps(data)
        response = requests.post(url=url, data=data, headers=headers)

        response = response.json()
        print("response", response)
        return res

    def _unlink_except_draft_or_cancel(self):
        print("hhhh")
        return super(InheritSale, self)._unlink_except_draft_or_cancel()




