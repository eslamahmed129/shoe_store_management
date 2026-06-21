import json
from odoo import http  # for using libray http
from odoo.http import request


class ProductApi(http.Controller):  # for inherit http controller
    # methods have 1-GET 2-POST 3-DELETE 4-PUT
    # type have http and json
    # you should make filter database in conf file
    # in postman you write localhost and port and route
    # in postman you write server host and port and route

    @http.route("/v1/product/json", methods=["POST"], type="json", auth="none", csrf=False)
    def post_product_json(self):
        args = request.httprequest.data.decode()  # for get data from api
        vals = json.loads(args)  # for convert data to dict
        res = 0
        if 'accessories' in vals:
            res = request.env['accessories'].sudo().create(vals)
        elif 'electricity' in vals:
            res = request.env['electricity'].sudo().create(vals)
        elif 'internal' in vals:
            res = request.env['internal'].sudo().create(vals)
        elif 'mobiles' in vals:
            res = request.env['mobiles'].sudo().create(vals)
        elif 'petrine_work' in vals:
            res = request.env['petrine_work'].sudo().create(vals)

        if res:
            return {  # return default json response
                "message": "The record has been created.",
                "id": res.id,
                "name": res.name,
            }

    @http.route("/v1/product", methods=["POST"], type="http", auth="none", csrf=False)
    def post_product(self):
        args = request.httprequest.data.decode()  # for get data from api
        vals = json.loads(args)  # for convert data to dict
        if not vals.get("name"):
            return request.make_json_response({
                "message": "The name is be required!",
            }, status=400)
        res = 0
        try:
            if 'accessories' in vals:
                res = request.env['accessories'].sudo().create(vals)
            elif 'electricity' in vals:
                res = request.env['electricity'].sudo().create(vals)
            elif 'internal' in vals:
                res = request.env['internal'].sudo().create(vals)
            elif 'mobiles' in vals:
                res = request.env['mobiles'].sudo().create(vals)
            elif 'petrine_work' in vals:
                res = request.env['petrine_work'].sudo().create(vals)

            if res:
                return request.make_json_response({  # for return json response
                    "message": "The record has been created.",
                    "id": res.id,
                    "name": res.name,
                }, status=200)
            else:
                return request.make_json_response({
                    "message": "You should enter category for product.",
                }, status=400)
        except Exception as error:
            if res:
                return request.make_json_response({
                    "message": "error"
                }, status=400)

    @http.route("/v1/product/accessories/<int:product_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_product(self, product_id):
        try:
            product_id = request.env['accessories'].sudo().search([('id', '=', product_id)])
            if not product_id:
                return request.make_json_response({
                    "message": "ID doesn't exist!",
                }, status=400)
            args = request.httprequest.data.decode()  # for get data from api
            vals = json.loads(args)  # for convert data to dict
            res = product_id.sudo().write(vals)
            return request.make_json_response({
                "message": "The record has been updated successfully.",
                "id": product_id.id,
                "name": product_id.name,
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "message": "error"
            }, status=400)

    @http.route("/v1/product/accessories/<int:product_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_product(self, product_id):
        try:
            product_id = request.env['accessories'].sudo().search([('id', '=', product_id)])
            if not product_id:
                return request.make_json_response({
                    "message": "ID doesn't exist!",
                }, status=400)
            return request.make_json_response({
                "id": product_id.id,
                "ref": product_id.ref,
                "name": product_id.name,
                "accessories": product_id.accessories,
                "price": product_id.price,
                "count": product_id.count,
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "message": "error"
            }, status=400)

    @http.route("/v1/product/accessories/<int:product_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_product(self, product_id):
        try:
            product_id = request.env['accessories'].sudo().search([('id', '=', product_id)])
            if not product_id:
                return request.make_json_response({
                    "message": "ID doesn't exist!",
                }, status=400)
            product_id.unlink()
            return request.make_json_response({
                "message": "The record has been deleted successfully.",
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "message": "error"
            }, status=400)






# import json
# from odoo import http  # for using library http
# from odoo.http import request
#
#
# class ShoeProductApi(http.Controller):  # for inherit http controller
#     # methods have 1-GET 2-POST 3-DELETE 4-PUT
#     # type have http and json
#     # you should make filter database in conf file
#     # in postman you write localhost and port and route
#
#     # =====================================================
#     # CREATE - Shoe Product
#     # =====================================================
#     @http.route("/v1/shoe/product", methods=["POST"], type="http", auth="none", csrf=False)
#     def post_shoe_product(self):
#         args = request.httprequest.data.decode()  # for get data from api
#         vals = json.loads(args)  # for convert data to dict
#
#         if not vals.get("name"):
#             return request.make_json_response({
#                 "message": "The name is required!",
#             }, status=400)
#
#         if not vals.get("gender"):
#             return request.make_json_response({
#                 "message": "The gender is required!",
#             }, status=400)
#
#         try:
#             # Handle size_ids and color_ids if sent as lists of IDs
#             if 'size_ids' in vals and isinstance(vals['size_ids'], list):
#                 vals['size_ids'] = [(6, 0, vals['size_ids'])]
#             if 'color_ids' in vals and isinstance(vals['color_ids'], list):
#                 vals['color_ids'] = [(6, 0, vals['color_ids'])]
#
#             res = request.env['shoe.product'].sudo().create(vals)
#
#             if res:
#                 return request.make_json_response({
#                     "message": "The record has been created.",
#                     "id": res.id,
#                     "name": res.name,
#                 }, status=200)
#             else:
#                 return request.make_json_response({
#                     "message": "Could not create the product.",
#                 }, status=400)
#         except Exception as error:
#             return request.make_json_response({
#                 "message": f"error: {str(error)}"
#             }, status=400)
#
#     # =====================================================
#     # READ - Single Shoe Product
#     # =====================================================
#     @http.route("/v1/shoe/product/<int:product_id>", methods=["GET"], type="http", auth="none", csrf=False)
#     def get_shoe_product(self, product_id):
#         try:
#             product = request.env['shoe.product'].sudo().search([('id', '=', product_id)])
#             if not product:
#                 return request.make_json_response({
#                     "message": "ID doesn't exist!",
#                 }, status=400)
#
#             return request.make_json_response({
#                 "id": product.id,
#                 "name": product.name,
#                 "default_code": product.default_code,
#                 "brand": product.brand,
#                 "gender": product.gender,
#                 "season": product.season,
#                 "list_price": product.list_price,
#                 "standard_price": product.standard_price,
#                 "variant_count": product.variant_count,
#                 "total_qty_available": product.total_qty_available,
#                 "sizes": product.size_ids.mapped('name'),
#                 "colors": product.color_ids.mapped('name'),
#             }, status=200)
#         except Exception as error:
#             return request.make_json_response({
#                 "message": f"error: {str(error)}"
#             }, status=400)
#
#     # =====================================================
#     # READ - All Shoe Products (list)
#     # =====================================================
#     @http.route("/v1/shoe/products", methods=["GET"], type="http", auth="none", csrf=False)
#     def get_all_shoe_products(self, **kwargs):
#         try:
#             products = request.env['shoe.product'].sudo().search([])
#             result = []
#             for product in products:
#                 result.append({
#                     "id": product.id,
#                     "name": product.name,
#                     "brand": product.brand,
#                     "gender": product.gender,
#                     "list_price": product.list_price,
#                     "variant_count": product.variant_count,
#                     "total_qty_available": product.total_qty_available,
#                 })
#             return request.make_json_response(result, status=200)
#         except Exception as error:
#             return request.make_json_response({
#                 "message": f"error: {str(error)}"
#             }, status=400)
#
#     # =====================================================
#     # UPDATE - Shoe Product
#     # =====================================================
#     @http.route("/v1/shoe/product/<int:product_id>", methods=["PUT"], type="http", auth="none", csrf=False)
#     def update_shoe_product(self, product_id):
#         try:
#             product = request.env['shoe.product'].sudo().search([('id', '=', product_id)])
#             if not product:
#                 return request.make_json_response({
#                     "message": "ID doesn't exist!",
#                 }, status=400)
#
#             args = request.httprequest.data.decode()
#             vals = json.loads(args)
#
#             if 'size_ids' in vals and isinstance(vals['size_ids'], list):
#                 vals['size_ids'] = [(6, 0, vals['size_ids'])]
#             if 'color_ids' in vals and isinstance(vals['color_ids'], list):
#                 vals['color_ids'] = [(6, 0, vals['color_ids'])]
#
#             product.sudo().write(vals)
#             return request.make_json_response({
#                 "message": "The record has been updated successfully.",
#                 "id": product.id,
#                 "name": product.name,
#             }, status=200)
#         except Exception as error:
#             return request.make_json_response({
#                 "message": f"error: {str(error)}"
#             }, status=400)
#
#     # =====================================================
#     # DELETE - Shoe Product
#     # =====================================================
#     @http.route("/v1/shoe/product/<int:product_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
#     def delete_shoe_product(self, product_id):
#         try:
#             product = request.env['shoe.product'].sudo().search([('id', '=', product_id)])
#             if not product:
#                 return request.make_json_response({
#                     "message": "ID doesn't exist!",
#                 }, status=400)
#
#             product.unlink()
#             return request.make_json_response({
#                 "message": "The record has been deleted successfully.",
#             }, status=200)
#         except Exception as error:
#             return request.make_json_response({
#                 "message": f"error: {str(error)}"
#             }, status=400)
#
#     # =====================================================
#     # GENERATE VARIANTS - Action endpoint
#     # =====================================================
#     @http.route("/v1/shoe/product/<int:product_id>/generate_variants", methods=["POST"], type="http", auth="none", csrf=False)
#     def generate_variants(self, product_id):
#         try:
#             product = request.env['shoe.product'].sudo().search([('id', '=', product_id)])
#             if not product:
#                 return request.make_json_response({
#                     "message": "ID doesn't exist!",
#                 }, status=400)
#
#             product.action_generate_variants()
#             return request.make_json_response({
#                 "message": "Variants generated successfully.",
#                 "variant_count": product.variant_count,
#             }, status=200)
#         except Exception as error:
#             return request.make_json_response({
#                 "message": f"error: {str(error)}"
#             }, status=400)
#
#     # =====================================================
#     # READ - Variants of a specific Product
#     # =====================================================
#     @http.route("/v1/shoe/product/<int:product_id>/variants", methods=["GET"], type="http", auth="none", csrf=False)
#     def get_product_variants(self, product_id):
#         try:
#             product = request.env['shoe.product'].sudo().search([('id', '=', product_id)])
#             if not product:
#                 return request.make_json_response({
#                     "message": "ID doesn't exist!",
#                 }, status=400)
#
#             result = []
#             for variant in product.variant_ids:
#                 result.append({
#                     "id": variant.id,
#                     "size": variant.size_id.name,
#                     "color": variant.color_id.name,
#                     "barcode": variant.barcode,
#                     "qty_available": variant.qty_available,
#                     "virtual_available": variant.virtual_available,
#                     "list_price": variant.list_price,
#                 })
#             return request.make_json_response(result, status=200)
#         except Exception as error:
#             return request.make_json_response({
#                 "message": f"error: {str(error)}"
#             }, status=400)
#
#     # =====================================================
#     # READ - Variant by Barcode (useful for scanner/POS)
#     # =====================================================
#     @http.route("/v1/shoe/variant/barcode/<string:barcode>", methods=["GET"], type="http", auth="none", csrf=False)
#     def get_variant_by_barcode(self, barcode):
#         try:
#             variant = request.env['shoe.product.variant'].sudo().search(
#                 [('barcode', '=', barcode)], limit=1
#             )
#             if not variant:
#                 return request.make_json_response({
#                     "message": "Barcode not found!",
#                 }, status=400)
#
#             return request.make_json_response({
#                 "id": variant.id,
#                 "product_name": variant.shoe_product_id.name,
#                 "size": variant.size_id.name,
#                 "color": variant.color_id.name,
#                 "qty_available": variant.qty_available,
#                 "list_price": variant.list_price,
#             }, status=200)
#         except Exception as error:
#             return request.make_json_response({
#                 "message": f"error: {str(error)}"
#             }, status=400)
#
#     # =====================================================
#     # UPDATE - Variant Stock/Price
#     # =====================================================
#     @http.route("/v1/shoe/variant/<int:variant_id>", methods=["PUT"], type="http", auth="none", csrf=False)
#     def update_variant(self, variant_id):
#         try:
#             variant = request.env['shoe.product.variant'].sudo().search([('id', '=', variant_id)])
#             if not variant:
#                 return request.make_json_response({
#                     "message": "ID doesn't exist!",
#                 }, status=400)
#
#             args = request.httprequest.data.decode()
#             vals = json.loads(args)
#
#             variant.sudo().write(vals)
#             return request.make_json_response({
#                 "message": "The variant has been updated successfully.",
#                 "id": variant.id,
#             }, status=200)
#         except Exception as error:
#             return request.make_json_response({
#                 "message": f"error: {str(error)}"
#             }, status=400)
#
#     # =====================================================
#     # DELETE - Variant
#     # =====================================================
#     @http.route("/v1/shoe/variant/<int:variant_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
#     def delete_variant(self, variant_id):
#         try:
#             variant = request.env['shoe.product.variant'].sudo().search([('id', '=', variant_id)])
#             if not variant:
#                 return request.make_json_response({
#                     "message": "ID doesn't exist!",
#                 }, status=400)
#
#             variant.unlink()
#             return request.make_json_response({
#                 "message": "The variant has been deleted successfully.",
#             }, status=200)
#         except Exception as error:
#             return request.make_json_response({
#                 "message": f"error: {str(error)}"
#             }, status=400)