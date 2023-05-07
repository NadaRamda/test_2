from odoo import http
from odoo.http import request,  Response
import json

token = "nada"

def _check_type(data=None, values=None):
    # invalid_date= []
    if values and data:
        for value in values:
            if type(value) != str or list:
                # invalid_date.append(value)
                return {
                    "code": "400",
                    "message": "Data is not valid "
                }


class Campany(http.Controller):

    def _check_required_values(self, data=None, keys=None):
        missing_value = []
        if data and keys:
            for key in keys:
                if not all([key in data, data.get(key)]):
                    missing_value.append(key)
                return missing_value or False

    @http.route('/api/post/createsaleorder/', auth='public', type='json', methods=['POST'])
    def create_saleorder(self, **kw):
        try:
            access_token = request.httprequest.headers['Authorization']
            if access_token != token:
                return {
                    'message': 'No valid token ',
                    'code': "401"
                }
            kw = request.httprequest.get_data()
            try:
                kw = json.loads(kw)
                required_value = ['CustomerCodeID', 'Lines']
                missing_value = self._check_required_values(data=kw, keys=required_value)
                if missing_value:
                    return {
                        'message': "missing parameters",
                        'code': "404"
                    }
            except ValueError:
                return {
                    'message': 'Invalid json data %r' % (request,),
                    'code': 400
                }
            order = []
            list = []
            for line in kw.get('Lines'):
                product_id = request.env['product.product'].sudo().search([('id', '=', line.get('Product_id'))])
                if product_id:
                    list.append((0, 0, {
                        'product_id': product_id.id,
                        'price_unit': line.get('Price_unit'),
                        'name': line.get('Description'),
                        'product_uom_qty': line.get('Qty')
                    })
                 )
                else:
                    response = {'code': 401, 'message': "No valid Product_id = " + str(line.get('Product_id'))}
                    return response

                partner_id = request.env['res.partner'].search([('name', '=', kw.get('CustomerName'))])
                if not partner_id:
                    partner_id = request.env['res.partner'].sudo().create({
                        "name": kw.get('CustomerName')
                    })
            order.append({
                "partner_id": partner_id.id,
                "order_line": list,
            })
            orders = http.request.env['sale.order'].sudo().create(order)
            data = {
                'CustomerName': orders.display_name,
                'CustomerID': orders.id,
                'TotalAmount': orders.amount_total,
                'TaxedAmount': orders.amount_tax,
                'UntaxedAmount': orders.amount_untaxed,
            }
            response = {"code": 200, "message": "Everything worked as expected", "data": data}
            return response
        except Exception as e:
            response = {"code": 400, "message": str(e)}
            return response

        # print("kw", kw)
        # print("kw", kw.get('CustomerCodeID'))
        # print("list", kw.get('Lines'))

    @http.route('/api/post/createbulksaleorder', auth='public', type='json', methods=['POST'])
    def create_bulksaleorder(self, **kw):
        try:
            access_token = request.httprequest.headers['Authorization']
            if access_token != token:
                return {
                    'message': 'No valid token ',
                    'code': "401"
                }
            kw = request.httprequest.get_data()
            try:
                kw = json.loads(kw)
                required_value = ['Data']
                missing_value = self._check_required_values(data=kw, keys=required_value)
                if missing_value:
                    return {
                        'message': "missing parameters %s !" % ', '.join(missing_value),
                        'code': "400"
                    }
            except ValueError:
                return {
                    'message': 'Invalid json data %r' % (request,),
                    'code': 400
                }
            data = []
            for k in kw['Data']:
                order = []
                list = []
                required_value_order = ['CustomerCodeID']
                missing_value_order = self._check_required_values(data=k, keys=required_value_order)
                if missing_value_order:
                    return {
                        'message': "missing parameters in order %s !" % ', '.join(missing_value_order),
                        'code': "400"
                    }
                for line in k.get('Lines'):
                    product_id = request.env['product.product'].sudo().search([('id', '=', line.get('Product_id'))])
                    if product_id:
                        list.append((0, 0, {
                            'product_id': product_id.id,
                            'price_unit': line.get('Price_unit'),
                            'name': line.get('Description'),
                            'product_uom_qty': line.get('Qty')

                        }))
                    else:
                        response = {'code': 401, 'message': "No valid Product_id = " + str(line.get('Product_id'))}
                        return response

                    partner_id = request.env['res.partner'].search([('name', '=', k.get('CustomerName'))])
                    if not partner_id:
                        partner_id = request.env['res.partner'].sudo().create({
                            "name": k.get('CustomerName')
                        })

                order.append({
                    "partner_id": partner_id.id,
                    "order_line": list,
                })

                orders = http.request.env['sale.order'].sudo().create(order)
                data.append({
                    'CustomerName': orders.display_name,
                    'CustomerID': orders.id,
                    'TotalAmount': orders.amount_total,
                    'TaxedAmount': orders.amount_tax,
                    'UntaxedAmount': orders.amount_untaxed,
                })
            if data:
                response = {"code": 200, "message": "Everything worked as expected", "data": data}
                return response
            else:
                response = {"code": 400,
                            "message": "We Are Facing a Problem Right Now Please Try Again in  a Few Seconds"}
            return response

        except Exception as e:
            response = {"code": 400, "message": str(e)}
            return response

    @http.route('/api/test_1/', auth='public', type='json', methods=['POST'])
    def index(self, **kw):
        print("kw", kw)
        # print(request.httprequest.headers['Authorization'])
        kw = request.httprequest.get_data()
        try:
            kw = json.loads(kw)
        except ValueError:
            return {
                'message': 'Invalid json data %r' % (request,),
                'code': 400
            }
        # access_token = kw.get('token', '')
        access_token = request.httprequest.headers['Authorization']
        # print(access_token)
        if access_token != token:
            return {
                'message': 'No valid token ',
                'code': 401
            }

        list_data = []

        data = {
            "Data": [
                {
                    "CustomerCodeID": 1,
                    "CustomerName": "nada",
                    "Lines": [
                        {
                            "Product_id": 1,
                            "Price_unit": 6,
                            "Description": "nada",
                            "Qty": 2
                        },
                        {
                            "Product_id": 1,
                            "Price_unit": 6,
                            "Description": "nada",
                            "Qty": 2
                        }
                    ]
                },
                {
                    "CustomerCodeID": 1,
                    "CustomerName": "nada",
                    "Lines": [
                        {
                            "Product_id": 2,
                            "Price_unit": 10,
                            "Description": "nada",
                            "Qty": 5
                        },
                        {
                            "Product_id": 2,
                            "Price_unit": 10,
                            "Description": "nada",
                            "Qty": 5
                        }
                    ]
                }
            ]

        }
        list_data.append(data)
        if data:
            return {
                "code": 200,
                "data": list_data
            }

    @http.route('/api/getsale/', auth='public', type='json', methods=['POST'])
    def getsale(self, **kw):
        kw = request.httprequest.get_data()
        try:
            kw = json.loads(kw)
        except ValueError:
            return {
                'message': 'Invalid json data %r' % (request,),
                'code': 400
            }
        # access_token = kw.get('token', '')
        access_token = request.httprequest.headers['Authorization']
        if access_token != token:
            return {
                'message': 'No valid token ',
                'code': 401
            }
        orders = request.env['sale.order.company'].sudo().search([])
        list = []
        for order in orders:
            vals = ({
                "partner_id": order.partner_id.name,
            })
            list.append(vals)
        print(list)
        if orders:
            return {
                "code": "100",
                "message": "success",
                "list": list,
            }
        else:
            return {
                "code": 404,
                "message": 'we are not have any data'
            }

    @http.route('/api/getsaleorder/', auth='public', type='json', methods=['POST'])
    def getsaleorder(self, **kw):
        kw = request.httprequest.get_data()
        try:
            kw = json.loads(kw)
        except ValueError:
            return {
                'message': 'Invalid json data %r' % (request,),
                'code': 400
            }
        # access_token = kw.get('token', '')
        access_token = request.httprequest.headers['Authorization']
        if access_token != token:
            return {
                'message': 'No valid token ',
                'code': 401
            }
        orders = request.env['sale.order'].sudo().search([('id', '=', 16)])
        list = []
        for order in orders:
            vals = ({
                "partner_id": order.partner_id.name,
                "date": order.date_order,
            })
            list.append(vals)
        print(list)
        if orders:
            return {
                "code": "100",
                "message": "success",
                "list": list,
            }
        else:
            return {
                "code": 404,
                "message": 'we are not have any data'
            }
