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

class account_analytic_account(osv.osv):
    _inherit = 'account.analytic.account' 
    _name = 'account.analytic.account'
    _columns = {
        'domains_url': fields.char('Dominios Vinculados', size=256),
        'project_type': fields.many2one('project.type','Servicio Recurrente'),
        'phone_partner' : fields.related('partner_id', 'phone', type="char", size=128, string="Telefono", readonly=True),
        'mail_partner': fields.related('partner_id', 'email', type='char', size=256,string='Email', readonly=True, help='Informacion proveniente del Cliente', ),
        'ref_created': fields.related('partner_id', 'ref_created', type='char', size=256,string='Ref Cliente', readonly=True, help='Informacion proveniente del Cliente', ),
    }




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
    'ref_order': fields.char('Referencia Pedido', type='char', size=256, readonly=True, help='Informacion proveniente del Cliente', ),
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
    
    ###### DISEÑO #####
    'estado_presupuesto': fields.many2one('project.states.quotation', 'Estado del Presupuesto'),
    'nombre_concretar': fields.many2one('project.nombre.concretar', 'Nombre por Concretar'),
    'tipo_disenio': fields.many2one('project.tipo.disenio', 'Tipo de Diseño'),
    'titulo_nombre_marca': fields.char('Titulo o nombre marca', size=128),
    'slogan': fields.char('Slogan', size=256),
    'perfil_potencial': fields.text('Perfil potencial del cliente'),
    
    'estilo_letra': fields.many2one('project.estilo.letra', 'Estilo de letra'),
    'ref_color1': fields.char('Ref color', size=128),
    'cromatismo': fields.many2one('project.cromatismo', 'Cromatismo'),
    'ref_color2': fields.char('Ref color', size=128),

    'estilos_fotos': fields.text('Estilos'),

    'recursos_ids': fields.one2many('project.recursos', 'project_id', 'Recursos'),

    'disenio_notas': fields.text('Notas'),

    }

    _defaults = {
        }
        
    _order = 'date_start'

    def create(self, cr, uid, vals, context=None):
        res = super(project_project, self).create(cr, SUPERUSER_ID, vals, context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        res = super(project_project, self).write(cr, SUPERUSER_ID, ids, vals, context)
        return res

class project_recursos(osv.osv):
    _name = 'project.recursos'
    _description = 'Recursos'
    _rec_name = 'datas_fname' 
    _columns = {
        'datas_fname': fields.char('File Name',size=256),
        'file':fields.binary('Recurso', required=True), 
        'project_id': fields.many2one('project.project', 'ID Ref'),
    }

class project_cromatismo(osv.osv):
    _name = 'project.cromatismo'
    _description = 'Estilo Letra'
    _columns = {
        'name':fields.char('Nombre', size=64, required=True), 
    }

class project_estilo_letra(osv.osv):
    _name = 'project.estilo.letra'
    _description = 'Estilo Letra'
    _columns = {
        'name':fields.char('Nombre', size=64, required=True), 
    }


class project_states_quotation(osv.osv):
    _name = 'project.states.quotation'
    _description = 'Estado Presupuesto'
    _columns = {
        'name':fields.char('Nombre', size=64, required=True), 
    }

class project_nombre_concretar(osv.osv):
    _name = 'project.nombre.concretar'
    _description = 'Nombre Concretar'
    _columns = {
        'name':fields.char('Nombre', size=64, required=True), 
    }

class project_tipo_disenio(osv.osv):
    _name = 'project.tipo.disenio'
    _description = 'Tipo Disenio'
    _columns = {
        'name':fields.char('Nombre', size=64, required=True), 
    }
 
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
    'ref_order': fields.char('Referencia Pedido', type='char', size=256, readonly=True, help='Informacion proveniente del Cliente', ),
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

    _order = 'date_start' 

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
        return super(project_task, self).unlink(cr, uid, ids, context=context)

    def onchange_project(self, cr, uid, id, project_id, context=None):
        res = super(project_task, self).onchange_project(cr, uid, id, project_id, context)
        if project_id:
            project = self.pool.get('project.project').browse(cr, uid, project_id, context=context)
            res['value'].update({'type_select': project.type_id.id})
        return res
        # if project_id:
        #     project = self.pool.get('project.project').browse(cr, uid, project_id, context=context)
        #     if project and project.partner_id:
        #         return {'value': {'partner_id': project.partner_id.id}}
        # return {}


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
    'task_created': fields.boolean('Tarea Creada',copy=False),
        }

    _defaults = {
        }

    # def create(self, cr, uid, vals, context=None):
    #     res = super(sale_order_line, self).create(cr, uid, vals, context)
    #     rec_br = self.browse(cr, uid, res, context)
    #     product_br = rec_br.product_id
    #     notas = rec_br.name
    #     extra_info_superficie = "SUPERFICIE: "+str(product_br.ancho)+" X "+str(product_br.alto)+ "COPIAS: "+str(product_br.cantidades_ancho_alto)
    #     extra_info_lineal = "MLINEAL: "+str(product_br.lado_1)+" + "+str(product_br.lado_2)+ "+ "+str(product_br.lado_3)+" + "+str(product_br.lado_4)
    #     notas = notas+"\n"+extra_info_superficie+"\n"+extra_info_lineal
    #     rec_br.write({'name':notas})
    #     return res

    # def copy(self, cr, uid, ids, default=None, context=None):
    #     default.update({
    #                     'task_created': False, 
    #                     })
    #     res = super(sale_order_line,self).copy(cr, uid, ids, default, context)
    #     return res

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
    
    def update_values_superficie(self, cr, uid, ids, context=None): 
        for rec in self.browse(cr, uid, ids, context):
            if 'MLINEAL' in rec.name:
                description = rec.product_id.default_code if rec.product_id.default_code else ''
                if description:
                    description = '['+description+'] '+rec.product_id.name            
                else:
                    description = rec.product_id.name
                notas = description
                product_br = rec.product_id
                extra_info_superficie = "SUPERFICIE: "+str(rec.ancho)+" X "+str(rec.alto)+ " COPIAS: "+str(rec.cantidades_ancho_alto)
                extra_info_lineal = "MLINEAL: "+str(rec.lado_1)+" + "+str(rec.lado_2)+ "+ "+str(rec.lado_3)+" + "+str(rec.lado_4)
                notas = notas+"\n"+extra_info_superficie+"\n"+extra_info_lineal
                rec.write({'name':notas})
                return True

            if not rec.name:
                description = rec.product_id.default_code if rec.product_id.default_code else ''
                if description:
                    description = '['+description+'] '+rec.product_id.name            
                else:
                    description = rec.product_id.name
            else:
                description = rec.name          
            notas = description
            product_br = rec.product_id
            extra_info_superficie = "SUPERFICIE: "+str(rec.ancho)+" X "+str(rec.alto)+ " COPIAS: "+str(rec.cantidades_ancho_alto)
            notas = notas+"\n"+extra_info_superficie
            # extra_info_lineal = "MLINEAL: "+str(rec.lado_1)+" + "+str(rec.lado_2)+ "+ "+str(rec.lado_3)+" + "+str(rec.lado_4)
            # notas = notas+"\n"+extra_info_superficie+"\n"+extra_info_lineal
            rec.write({'name':notas})
        return True

    def update_values_lineal(self, cr, uid, ids, context=None): 
        for rec in self.browse(cr, uid, ids, context):
            if 'SUPERFICIE' in rec.name:
                description = rec.product_id.default_code if rec.product_id.default_code else ''
                if description:
                    description = '['+description+'] '+rec.product_id.name            
                else:
                    description = rec.product_id.name
                notas = description
                product_br = rec.product_id
                extra_info_superficie = "SUPERFICIE: "+str(rec.ancho)+" X "+str(rec.alto)+ " COPIAS: "+str(rec.cantidades_ancho_alto)
                extra_info_lineal = "MLINEAL: "+str(rec.lado_1)+" + "+str(rec.lado_2)+ "+ "+str(rec.lado_3)+" + "+str(rec.lado_4)
                notas = notas+"\n"+extra_info_superficie+"\n"+extra_info_lineal
                rec.write({'name':notas})
                return True

            if not rec.name:
                description = rec.product_id.default_code if rec.product_id.default_code else ''
                if description:
                    description = '['+description+'] '+rec.product_id.name            
                else:
                    description = rec.product_id.name
            else:
                description = rec.name          
            notas = description
            product_br = rec.product_id
            #extra_info_superficie = "SUPERFICIE: "+str(rec.ancho)+" X "+str(rec.alto)+ "COPIAS: "+str(rec.cantidades_ancho_alto)
            extra_info_lineal = "MLINEAL: "+str(rec.lado_1)+" + "+str(rec.lado_2)+ "+ "+str(rec.lado_3)+" + "+str(rec.lado_4)
            notas = notas+"\n"+extra_info_lineal
            # notas = notas+"\n"+extra_info_superficie+"\n"+extra_info_lineal
            rec.write({'name':notas})
        return True

    # def create(self, cr, uid, vals, context=None):
    #     res = super(sale_order_line, self).create(cr, uid, vals, context)
    #     self.update_values_superficie_lineal(cr, uid, [res], context)
    #     return res

class sale_order(osv.osv):
    _name = 'sale.order'
    _inherit ='sale.order'
    _columns = {
        'ref_order': fields.char('Referencia Pedido', type='char', size=256, help='Informacion proveniente del Cliente', ),
        'quotation_status': fields.selection([('Pendiente','Pendiente'),('Aprobado','Aprobado')],'Situacion de Presupuesto', track_visibility="onchange"),
        'oportunity_origin': fields.many2one('crm.lead', 'Oportunidad Origen'),
        'phone_partner' : fields.related('partner_id', 'phone', type="char", size=128, string="Telefono", readonly=True),
        'mail_partner': fields.related('partner_id', 'email', type='char', size=256,string='Email', readonly=True, help='Informacion proveniente del Cliente', ),
        'ref_created': fields.related('partner_id', 'ref_created', type='char', size=256,string='Ref Cliente', readonly=True, help='Informacion proveniente del Cliente', ),
        }

    _defaults = {
        'pricelist_id': False,
        }

    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        res = super(sale_order, self).onchange_partner_id(cr, uid, ids, part, context)
        res['value'].update({'pricelist_id':False})
        return res

    # def create(self, cr, uid, vals, context=None):
    #     res = super(sale_order, self).create(cr, uid, vals, context)
    #     rec_br = self.browse(cr, uid, res, context)
    #     for line in rec_br.order_line:
    #         line.update_values_superficie_lineal()
    #     return res

    def default_get(self, cr, uid, fields, context = None):
        rs = super(sale_order, self).default_get(cr, uid, fields, context)
        rs['pricelist_id'] = False
        return rs

class crm_make_sale(osv.osv_memory):
    _name = 'crm.make.sale'
    _inherit ='crm.make.sale'
    _columns = {
        }

    _defaults = {
        }

    def makeOrder(self, cr, uid, ids, context=None):
        """
        This function  create Quotation on given case.
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of crm make sales' ids
        @param context: A standard dictionary for contextual values
        @return: Dictionary value of created sales order.
        """
        # update context: if come from phonecall, default state values can make the quote crash lp:1017353
        context = dict(context or {})
        context.pop('default_state', False)        
        
        case_obj = self.pool.get('crm.lead')
        sale_obj = self.pool.get('sale.order')
        partner_obj = self.pool.get('res.partner')
        data = context and context.get('active_ids', []) or []

        for make in self.browse(cr, uid, ids, context=context):
            partner = make.partner_id
            partner_addr = partner_obj.address_get(cr, uid, [partner.id],
                    ['default', 'invoice', 'delivery', 'contact'])
            pricelist = partner.property_product_pricelist.id
            fpos = partner.property_account_position and partner.property_account_position.id or False
            payment_term = partner.property_payment_term and partner.property_payment_term.id or False
            new_ids = []
            for case in case_obj.browse(cr, uid, data, context=context):
                if not partner and case.partner_id:
                    partner = case.partner_id
                    fpos = partner.property_account_position and partner.property_account_position.id or False
                    payment_term = partner.property_payment_term and partner.property_payment_term.id or False
                    partner_addr = partner_obj.address_get(cr, uid, [partner.id],
                            ['default', 'invoice', 'delivery', 'contact'])
                    pricelist = partner.property_product_pricelist.id
                if False in partner_addr.values():
                    raise osv.except_osv(_('Insufficient Data!'), _('No address(es) defined for this customer.'))

                vals = {
                    'origin': _('Opportunity: %s') % str(case.id),
                    'oportunity_origin': case.id,
                    'section_id': case.section_id and case.section_id.id or False,
                    'categ_ids': [(6, 0, [categ_id.id for categ_id in case.categ_ids])],
                    'partner_id': partner.id,
                    'pricelist_id': pricelist,
                    'partner_invoice_id': partner_addr['invoice'],
                    'partner_shipping_id': partner_addr['delivery'],
                    'date_order': fields.datetime.now(),
                    'fiscal_position': fpos,
                    'payment_term':payment_term,
                    'note': sale_obj.get_salenote(cr, uid, [case.id], partner.id, context=context),
                }
                if partner.id:
                    vals['user_id'] = partner.user_id and partner.user_id.id or uid
                new_id = sale_obj.create(cr, uid, vals, context=context)
                sale_order = sale_obj.browse(cr, uid, new_id, context=context)
                case_obj.write(cr, uid, [case.id], {'ref': 'sale.order,%s' % new_id})
                new_ids.append(new_id)
                message = _("Opportunity has been <b>converted</b> to the quotation <em>%s</em>.") % (sale_order.name)
                case.message_post(body=message)
            if make.close:
                case_obj.case_mark_won(cr, uid, data, context=context)
            if not new_ids:
                return {'type': 'ir.actions.act_window_close'}
            if len(new_ids)<=1:
                value = {
                    'domain': str([('id', 'in', new_ids)]),
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'sale.order',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'name' : _('Quotation'),
                    'res_id': new_ids and new_ids[0]
                }
            else:
                value = {
                    'domain': str([('id', 'in', new_ids)]),
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'sale.order',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'name' : _('Quotation'),
                    'res_id': new_ids
                }
            return value

class account_analytic_account(osv.osv):
    _name = 'account.analytic.account'
    _inherit ='account.analytic.account'

    def _total_subtotal(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        total = 0.0
        subtotal = 0.0
        for rec in self.browse(cr, uid, ids, context):
            for line in rec.recurring_invoice_line_ids:
                subtotal+= line.price_subtotal
            res[rec.id] = subtotal
        return res 
    _columns = {

    'subtotal': fields.function(_total_subtotal,  digits=(14,2),  string="Total a Facturar"),
        }

    _defaults = {
        }