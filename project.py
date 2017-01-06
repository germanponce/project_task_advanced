# -*- coding: utf-8 -*-
#
# German Ponce Dominguez
#
#

from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import datetime, timedelta
import time
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import SUPERUSER_ID

# class purchase_task_wizard(osv.osv_memory):
#     _name = 'purchase.task.wizard'
#     _description = 'Asistente de creacion de Tareas'
#     _columns = {
#     'product_id': fields.many2one('product.product','Producto', readonly=True),

#     }
#     _defaults = {  

#         }

#     def _get_product(self, cr, uid, context=None):
#         product_id = False
#         active_ids = context['active_ids']
#         if active_ids:
#             sale_order_line = self.pool.get('sale.order.line')
#             sale_order_line_br = sale_order_line.browse(cr, uid, active_ids, context)[0]
#             product_id = sale_order_line_br.product_id.id
#         return product_id

#     _defaults = {  
#         'product_id': _get_product,
#         }

#     def process_task(self, cr, uid, ids, context=None):
#         active_ids = context['active_ids']
#         sale_order_line = self.pool.get('sale.order.line')
#         project_obj = self.pool.get('project.project')
#         project_task_obj = self.pool.get('project.task')
#         task_id = False
#         for sale in sale_order_line.browse(cr, uid, active_ids, context):
#             # if sale.order_id.state in ('draft','cancel'):
#             #     raise except_orm(_('Error !'), 
#             #                      _('El Pedido se encuentra en Borrador o Cancelado, deberia estar Confirmado.'))

#             project_search = project_obj.search(cr, uid, [('name','=',sale.name)])
#             project_id = False
#             if project_search:
#                 project_id = project_search[0]
#             else:
#                 project_vals = {
#                     'name': sale.name,
#                     'user_id': sale.order_id.user_id.id if sale.order_id.user_id else False,
#                     'partner_id': sale.order_id.partner_id.id,
#                 }
#                 project_id = project_obj.create(cr, uid, project_vals, context)
#             if sale.task_created:
#                 raise except_orm(_('Error !'), 
#                                   _('Esta Linea ya tiene asignada una Tarea!'))

#             task_vals  = {
#                 'project_id': project_id,
#                 'partner_id': sale.order_id.partner_id.id,
#                 'product_description': sale.name,
#                 'name': sale.name,
#                 'qty': sale.product_uom_qty,
#                 'uom_id': sale.product_uom.id,
#                 'product_id': sale.product_id.id,
#                 'line_id': sale.id,
#                 'user_id': sale.order_id.user_id.id,
#                 'state':'curse',
#             }
#             task_id = project_task_obj.create(cr, uid, task_vals, context)
#             sale.write({'task_created': True})

#         return {
#                 'type': 'ir.actions.act_window',
#                 'name': _('Tarea Nueva'),
#                 'res_model': 'project.task',
#                 'res_id': task_id, ### Un Solo ID
#                 'view_type': 'form',
#                 'view_mode': 'form',
#                 'view_id': False,
#                 'target': 'current',
#                 #'target': 'new',
#                 'nodestroy': True,
#             }
class project_project_photos(osv.osv):
    _name = 'project.project.photos'
    _description = 'Descripcion del Modelo'
    _columns = {
        'photo': fields.binary('Fotografia'),
        'project_id': fields.many2one('project.project','ID Ref')
    }


class project_project(osv.osv):
    _name = 'project.project'
    _inherit ='project.project'


    _columns = {
    'ref_order': fields.char('Referencia Cliente', type='char', size=256, readonly=True, help='Informacion proveniente del Cliente', ),
    'photo_ids': fields.one2many('project.project.photos','project_id', 'Fotografias'),
    ## Publicidad Exterior ###
    'notas1': fields.char('Notas/Medidas', size=256),
    'notas2': fields.char('Notas/Medidas', size=256),
    'notas3': fields.char('Notas/Medidas', size=256),
    'notas4': fields.char('Notas/Medidas', size=256),
    'address': fields.text('Direcciond de montaje'),
    'cliente': fields.char('Cliente', size=256),
    'direccion_obra': fields.char('Direccion Obra', size=256),
    'electricista': fields.char('Electricista', size=256),
    'constructor': fields.char('Constructor', size=256),
    'pub_notas': fields.text('Notas', size=256),


    ## Diseño Web ###
    'url_admin': fields.char('URL Admin', size=256),
    'usuario': fields.char('Usuario', size=256),
    'contrasenia': fields.char('Contraseña', size=256),

    ## SEO ###
    'keyword1': fields.char('Keyword 1', size=256),
    'keyword2': fields.char('Keyword 2', size=256),
    'keyword3': fields.char('Keyword 3', size=256),
    'keyword4': fields.char('Keyword 4', size=256),
    ## Hosting ##
    'proveedor_dominio': fields.char('Proveedor Dominio', size=256),
    'usuario_hosting': fields.char('Usuario', size=256),
    'contrasenia_hosting': fields.char('Contraseña', size=256),
    'ip_servidor': fields.char('IP Servidor', size=256),
    'proveedor_hosting': fields.char('Proveedor Hosting', size=256),
    'usuario_servidor_hosting': fields.char('Usuario', size=256),
    'contrasenia_servidor_hosting': fields.char('Contraseña', size=256),
    'usuario_servidor_ftp': fields.char('Usuario', size=256),
    'contrasenia_servidor_ftp': fields.char('Contraseña', size=256),
    'usuario_servidor_bd': fields.char('Usuario', size=256),
    'contrasenia_servidor_bd': fields.char('Contraseña', size=256),
    'bd_name': fields.char('Base de Datos', size=256),
    'bd_url': fields.char('URL Acceso MySQL', size=256),
    'dominio1': fields.char('Dominio', size=256),
    'dominio2': fields.char('Dominio', size=256),
    'dominio3': fields.char('Dominio', size=256),
    'redirigido1': fields.char('Redirigido hacia', size=256),
    'redirigido2': fields.char('Redirigido hacia', size=256),
    'redirigido3': fields.char('Redirigido hacia', size=256),

    'url_marketing1': fields.char('URL Acceso', size=256),
    'usuario_marketing1': fields.char('Usuario', size=256),
    'contrasenia_marketing1': fields.char('Contraseña', size=256),
    'url_marketing2': fields.char('URL Acceso', size=256),
    'usuario_marketing2': fields.char('Usuario', size=256),
    'contrasenia_marketing2': fields.char('Contraseña', size=256),
    'url_marketing3': fields.char('URL Acceso', size=256),
    'usuario_marketing3': fields.char('Usuario', size=256),
    'contrasenia_marketing3': fields.char('Contraseña', size=256),
    'url_marketing4': fields.char('URL Acceso', size=256),
    'usuario_marketing4': fields.char('Usuario', size=256),
    'contrasenia_marketing4': fields.char('Contraseña', size=256),
        }

    _defaults = {
        }

    def create(self, cr, uid, vals, context=None):
        res = super(project_project, self).create(cr, SUPERUSER_ID, vals, context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        res = super(project_project, self).write(cr, SUPERUSER_ID, ids, vals, context)
        return res

class project_task(osv.osv):
    _name = 'project.task'
    _inherit ='project.task'
    def _total_taxes(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        total = 0.0
        subtotal = 0.0
        for rec in self.browse(cr, uid, ids, context):
            for line in rec.cost_ids:
                total+= line.subtotal
                subtotal+= line.qty*line.price
            res[rec.id] = total - subtotal
        return res 
    def _total_subtotal(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        total = 0.0
        subtotal = 0.0
        for rec in self.browse(cr, uid, ids, context):
            for line in rec.cost_ids:
                total+= line.subtotal
                subtotal+= line.qty*line.price
            res[rec.id] = subtotal
        return res 
    def _total_total(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        total = 0.0
        for rec in self.browse(cr, uid, ids, context):
            for line in rec.cost_ids:
                total+= line.subtotal
            res[rec.id] = total
        return res 

    _columns = {
    'ref_order': fields.char('Referencia Cliente', type='char', size=256, readonly=True, help='Informacion proveniente del Cliente', ),
    'line_id': fields.many2one('sale.order.line', 'Linea Origen'),
    'order_id': fields.many2one('sale.order', 'Pedido Origen'),
    'state': fields.selection([('draft','Borrador'),('curse','Curso'),('done','Finalizado'),('cancel','Cancelado')], 'Estado', track_visibility='onchange'),
    'execute_date': fields.date('Fecha Ejecucion'),
    ### Campos Calculados ####
    'total_taxes': fields.function(_total_taxes,  digits=(14,2),  string="Impuestos"),
    'subtotal': fields.function(_total_subtotal,  digits=(14,2),  string="Impuestos"),
    'total': fields.function(_total_total,  digits=(14,2),  string="Impuestos"),

    'phone_partner' : fields.related('partner_id', 'phone', type="char", size=128, string="Telefono", readonly=True),
    'mail_partner': fields.related('partner_id', 'email', type='char', size=256,string='Email', readonly=True, help='Informacion proveniente del Cliente', ),
    'ref_created': fields.related('partner_id', 'ref_created', type='char', size=256,string='Ref Cliente', readonly=True, help='Informacion proveniente del Cliente', ),
    'production_file': fields.char('Ruta archivo produccion', size=256),
    
    'product_description': fields.char('Descripcion Producto', size=256),
    'qty': fields.float('Cantidad Presupuestada', digits=(14,2)),
    'uom_id': fields.many2one("product.uom", 'Unidad'),
    'product_id': fields.many2one('product.product', 'Producto'),
    'subcontratacion_id': fields.many2one('res.partner', 'Subcontratacion'),
    'type_select': fields.many2one('project.type', 'Tipo'),
    'cost_ids': fields.one2many('project.task.costs', 'task_id', 'Costos'),
    'currency_id': fields.many2one('res.currency', 'Moneda'),
    'alto': fields.float('Alto', digits=(14,2)),
    'ancho': fields.float('Ancho', digits=(14,2)),
    'copias': fields.float('Copias', digits=(14,2)),
    'sangrado': fields.float('Sangrado', digits=(14,2)),
    'more_details': fields.text('Mas detalles'),
    }

    def _get_currency(self, cr, uid, context=None):
        currency_id = False
        user_br = self.pool.get('res.users').browse(cr, uid, uid, context)
        currency_id = user_br.company_id.currency_id.id
        return currency_id

    _defaults = {
    'currency_id': _get_currency,
    'state': 'draft',
        }

    _order = 'id asc' 

    def button_dummy(self, cr, uid, ids, context=None):
        return True

    def draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'draft'})

    def curse(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'curse'})

    def done(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'done','date_last_stage_update':time.strftime('%Y-%m-%d'),})

    def cancel(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'cancel'})

    def unlink(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids, context):
            if rec.line_id:
                rec.line_id.write({'task_created':False})
        return super(project_task, self).create(cr, uid, values, context=context)

class project_task_costs(osv.osv):
    _name = 'project.task.costs'
    _description = 'Costos'
    _rec_name = 'product_id'

    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        user_obj = self.pool.get('res.users')
        res = {}
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            price = line.price 
            taxes = tax_obj.compute_all(cr, uid, line.tax_id, price, line.qty, line.product_id, False)
            cur = user_obj.browse(cr, uid,uid).company_id.currency_id
            #cur = line.order_id.pricelist_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total_included'])
        return res
            
    def onchange_product_id(self, cr, uid, ids, product, qty, price, context=None):
        if not product:
             return {'value': {}}
        product_rec = self.pool.get('product.product').browse(cr, uid, product, context=context)

        taxes = product_rec.taxes_id 
        if price:
            subtotal = qty*price
        else:
            subtotal = product_rec.lst_price*price
        desccripcion = product_rec.default_code if product_rec.default_code else ''
        desccripcion = '['+desccripcion+'] '+product_rec.name
        val = {
            'name': desccripcion,
            'tax_id':taxes,
            'price':product_rec.lst_price if not price else price,
            'subtotal': subtotal,
            'product_uom': product_rec.uom_id.id,
        }
        return {'value': val} 


    _columns = {
        'task_id': fields.many2one('project.task', 'ID Ref'),
        'product_id': fields.many2one('product.product', 'Producto'),
        'name': fields.char('Descripcion', size=256),
        'product_uom': fields.many2one('product.uom', 'Unidad'),
        'qty': fields.float('Cantidad', digits=(14,2)),
        'price': fields.float('Precio', digits=(14,2)),
        'subtotal': fields.function(_amount_line, string='Subtotal', digits=(14,2)),
        'tax_id': fields.many2many('account.tax', 'cost_task_producto_tax', 'cost', 'tax_id','Impuestos'),
    }

    _defaults = {  
        'qty': 1.0,
        }

class sale_order_line(osv.osv):
    _name = 'sale.order.line'
    _inherit ='sale.order.line'
    _columns = {
    'task_created': fields.boolean('Tarea Creada'),
        }

    _defaults = {
        }

    def process_task(self, cr, uid, ids, context=None):
        sale_order_line = self.pool.get('sale.order.line')
        project_obj = self.pool.get('project.project')
        project_task_obj = self.pool.get('project.task')
        task_id = False
        for sale in self.browse(cr, uid, ids, context):
            # if sale.order_id.state in ('draft','cancel'):
            #     raise except_orm(_('Error !'), 
            #                      _('El Pedido se encuentra en Borrador o Cancelado, deberia estar Confirmado.'))

            project_search = project_obj.search(cr, uid, [('name','=',sale.order_id.name)])
            project_id = False
            if project_search:
                project_id = project_search[0]
            else:
                project_vals = {
                    'name': sale.order_id.name,
                    'user_id': sale.order_id.user_id.id if sale.order_id.user_id else False,
                    'partner_id': sale.order_id.partner_id.id,
                    'ref_order':sale.order_id.client_order_ref,
                }
                project_id = project_obj.create(cr, uid, project_vals, context)
            if sale.task_created:
                raise except_orm(_('Error !'), 
                                  _('Esta Linea ya tiene asignada una Tarea, si desea modificarla es necesario eliminar la tarea relacionada.'))

            task_vals  = {
                'project_id': project_id,
                'partner_id': sale.order_id.partner_id.id,
                'product_description': sale.name,
                'name': sale.name,
                'qty': sale.product_uom_qty,
                'uom_id': sale.product_uom.id,
                'product_id': sale.product_id.id,
                'line_id': sale.id,
                'order_id': sale.order_id.id,
                'user_id': sale.order_id.user_id.id,
                'state':'curse',
                'ref_order':sale.order_id.client_order_ref,
            }
            task_id = project_task_obj.create(cr, uid, task_vals, context)
            sale.write({'task_created': True})

        return {
                'type': 'ir.actions.act_window',
                'name': _('Tarea Nueva'),
                'res_model': 'project.task',
                'res_id': task_id, ### Un Solo ID
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': False,
                'target': 'current',
                #'target': 'new',
                'nodestroy': True,
            }

class sale_order(osv.osv):
    _name = 'sale.order'
    _inherit ='sale.order'
    _columns = {
    'ref_order': fields.char('Referencia Pedido', type='char', size=256, help='Informacion proveniente del Cliente', ),
    'quotation_status': fields.selection([('Pendiente','Pendiente'),('Curso','Curso'),('Aprobado','Aprobado'),('Cancelado','Cancelado')],'Situacion de Presupuesto', track_visibility="onchange"),
        }

    _defaults = {
        }