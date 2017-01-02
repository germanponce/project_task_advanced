# -*- coding: utf-8 -*-
#
# Daniel Maraboli
#
#

from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import datetime, timedelta
import time
from openerp.exceptions import except_orm, Warning, RedirectWarning

#### HERENCIA DE COMPRAS
class purchase_order(osv.osv):
    _name = 'purchase.order'
    #herencia de compras
    _inherit ='purchase.order'
    _columns = {
        'project_home_id': fields.many2one('project.home', 'Proyecto Inmobiliario'),
        'project_home': fields.boolean('Proyecto Inmobiliario'),

        }

    _defaults = {
        }

#### LINEAS DE COTIZACION
class project_home_line(osv.osv):
    _name = 'project.home.line'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Lineas Proyecto Cotizacion Inmobiliaria'

    #### OBTENER SUBTOTALES
    def _obtener_subtotal(self, cr, uid,
        ids, field_name, arg, context=None):
        res = {}
        subtotal=0.0
        #instancias de modelos
        user_br = self.pool.get('res.users').browse(cr, uid, uid, context)
        currency_id  = user_br.company_id.currency_id.id
        cur_obj=self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        for line in self.browse(cr, uid, ids, context=context):
            taxes = tax_obj.compute_all(cr, uid, 
                line.taxes_id, line.price, line.qty, 
                line.product_id, user_br.company_id.partner_id)
            cur = user_br.company_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
        return res
    #declaracion de variables
    _columns = {
        'project_home_id': fields.many2one('project.home', 'Proyecto Inmobiliario'),
        'product_id': fields.many2one('product.product','Insumo', required=True),
        'product_uom': fields.many2one('product.uom','UdM', required=True),
        'name': fields.char('Actividad', size=128, required=True),
        'qty': fields.float('Cantidad', digits=(14,2), required=True),
        'price': fields.float('Precio', digits=(14,2), required=True),
        'taxes_id': fields.many2many('account.tax', 'purchase_order_taxe_project_home', 'project_id', 'tax_id', 'Impuestos'),
        'subtotal': fields.function( _obtener_subtotal,
        string="Subtotal", type="float", digits=(14,2), store=True),
            }

    def on_change_product(self, cr, uid, ids, product_id, context=None):
        res = {}
        if not product_id:
            return {}
        prod_br = self.pool.get('product.product').browse(cr, uid, product_id, context)
        res.update({
            'product_uom': prod_br.uom_id.id,
            'price': prod_br.list_price,
            'taxes_id': [(6,0,[p.id for p in prod_br.taxes_id ])] 
            })
        return {'value': res}


    def product_uom_change(self, cr, uid, ids, product_uom, product_id, context=None):
        context = context or {}
        product_uom_obj = self.pool.get('product.uom')
        partner_obj = self.pool.get('res.partner')
        product_obj = self.pool.get('product.product')

        if not product_id:
            return {'value': {}, 'domain': {'product_uom': []}}

        result = {}
        domain = {}
        warning_msgs = ''
        product_obj = product_obj.browse(cr, uid, product_id, context)

        uom2 = False
        uom = product_uom
        if uom:
            uom2 = product_uom_obj.browse(cr, uid, uom)
            if product_obj.uom_id.category_id.id != uom2.category_id.id:
                uom = False

        if not uom:
            result['product_uom'] = product_obj.uom_id.id
            if product_obj.uos_id:
                uos_category_id = product_obj.uos_id.category_id.id
            else:
                uos_category_id = False
            domain = {'product_uom':
                        [('category_id', '=', product_obj.uom_id.category_id.id)],
                        }

        return {'value': result, 'domain': domain}

#### PROYECTO INMOBILIARIA CLASE PRINCIPAL
class project_home(osv.osv):
    _name = 'project.home'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Proyecto Cotizacion Inmobiliaria'
    
    def _obtener_total(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj=self.pool.get('res.currency')
        tax_obj= self.pool.get('account.tax')
        user_br = self.pool.get('res.users').browse(cr, uid, uid, context)
        currency_id  = user_br.company_id.currency_id.id
        res = {}
        subtotal_line_global = 0.0
        for order in self.browse(cr, uid, ids, context=context):
            home_number =  order.home_number if order.home_number > 0 else 1 #se asigna la cant de vivienda si es mayor a 0
            res[order.id] = {
                'tax_amount': 0.0,
                'subtotal': 0.0,
                'total': 0.0,
                }
            val = val1 = 0.0
            cur = order.currency_id
            for line in order.home_line:
                val1 += line.subtotal
                taxes = tax_obj.compute_all(cr, uid, 
                    line.taxes_id, line.price, line.qty, 
                    line.product_id, user_br.company_id.partner_id)
                cur = user_br.company_id.currency_id
                subtotal_line = cur_obj.round(cr, uid, cur, taxes['total'])
                subtotal_line_global += subtotal_line
                for c in self.pool.get('account.tax').compute_all(cr, uid, line.taxes_id, line.price, line.qty, line.product_id, user_br.company_id.partner_id)['taxes']:
                    val += c.get('amount', 0.0)
            res[order.id]['tax_amount']=(cur_obj.round(cr, uid, cur, val) ) * home_number #multiplica el iva * viviendas
            res[order.id]['subtotal']= subtotal_line_global * home_number  #multiplica el subtotal de productos * viviendas
            res[order.id]['total']=( res[order.id]['subtotal'] + res[order.id]['tax_amount'] ) #se obtiene el total suma de la multiplicacion

        return res
     #declaracion de variables
    _columns = {
    'home_line': fields.one2many('project.home.line','project_home_id','Lineas Presupuesto'),
    'name': fields.char('Descripcion', size=128, 
        required=True),
    'location': fields.char('Ubicacion', size=128, 
        required=True),
    'active': fields.boolean('Activo'),
    'state': fields.selection([('nuevo','Nuevo'),
                            ('confirmado','Confimado'),
                            ('hecho','Hecho'),
                            ('cancelado','Cancelado')], string="Estado"),
    'order_id': fields.many2one('purchase.order','Compra',
        help='Orden de Compra Relacionado con este Proyecto', ),
    'sequence': fields.char('Secuencia', size=128),
    'notas': fields.text('Notas'),
    'home_number': fields.integer('Viviendas', required=True),
    'date': fields.date('Fecha', required=True),
    'supplier_id': fields.many2one('res.partner','Proveedor'),
    ### CAMPOS CALCULADOS 
    'tax_amount': fields.function( _obtener_total,
    string="Impuestos", type="float", digits=(14,2), store=True, multi="calculos"),
    'subtotal': fields.function( _obtener_total,
    string="Subtotal", type="float", digits=(14,2), store=True, multi="calculos"),
    'total': fields.function( _obtener_total,
    string="Total", type="float", digits=(14,2), store=True, multi="calculos"),
    'currency_id': fields.many2one('res.currency', 'Moneda'),
    }
    
    def button_dummy(self, cr, uid, ids, context=None):
        return True

    def _get_cur(self, cr, uid, context=None):
        currency_id = False
        user_br = self.pool.get('res.users').browse(cr, uid, uid, context)
        currency_id  = user_br.company_id.currency_id.id
        return currency_id

    _defaults = {
    'date': time.strftime('%Y-%m-%d'),
    'active': True,
    'state':'nuevo',
    'currency_id': _get_cur,
        }

    _order = 'sequence'  # Order de Registros

    def confirmar(self, cr, uid, ids, context=None):
        # self.write(cr, uid, ids, 
        #     {'state':'inscrito'}, context)
        for rec in self.browse(cr, uid, ids, context):
            rec.write({'state':'confirmado'})
            rec.message_post(
            body=_("%s Cambio al Estado \
             <b><em>Confirmado</em></b>." % rec.sequence))
        return True

    ## CAMBIA EL ESTADO A REALIZADO Y CREA EL PEDIDO DE COMPRA
    def finalizar(self, cr, uid, ids, context=None):
        # self.write(cr, uid, ids, 
        #     {'state':'inscrito'}, context)
        order_obj = self.pool.get('purchase.order') #instancias
        user_br = self.pool.get('res.users').browse(cr, uid, uid, context)
        for rec in self.browse(cr, uid, ids, context):
            # lines = []
            # home_number =  rec.home_number if rec.home_number > 0 else 1
            # if not rec.supplier_id:
            #     raise except_orm(_('Error !'), 
            #         _('Necesitas definir un Proveedor para Generar la Orden de Compra, proyecto ' + rec.sequence))
            # if not rec.home_line:
            #     raise except_orm(_('Error !'), 
            #         _('Necesitas al menos una linea de Presupuesto para generar la Orden de Compra, proyecto ' + rec.sequence))
            # for line in rec.home_line:
            #     xline = (0,0,{
            #         'product_id': line.product_id.id,
            #         'name': line.name,
            #         'date_planned': rec.date,
            #         'company_id': user_br.company_id.id,
            #         'product_qty': line.qty * home_number,
            #         'product_uom': line.product_uom.id,
            #         'price_unit': line.price,
            #         'tax_id': [(6,0,[p.id for p in line.taxes_id ])],
            #         })
            #     lines.append(xline)
            # address = self.pool.get('res.partner')
            # supplier = address.browse(cr, uid, rec.supplier_id.id, context=context)
            # location_id = supplier.property_stock_customer.id
            # vals = {
            #     'partner_id': rec.supplier_id.id,
            #     'narration': rec.notas,
            #     'origin': rec.sequence,
            #     'order_line': [x for x in lines],
            #     'company_id': user_br.company_id.id,
            #     'invoice_method': 'order',
            #     'location_id': user_br.company_id.partner_id.property_stock_customer.id,
            #     'project_home_id': rec.id,
            #     'currency_id': rec.currency_id.id,
            #     'pricelist_id': supplier.property_product_pricelist_purchase.id,
            #     'dest_address_id': user_br.company_id.partner_id.id,
            #     'project_home': True,
            # }
            # order_id = order_obj.create(cr, uid, vals, context)
            # order_br = order_obj.browse(cr, uid, order_id, context)
            # rec.write({'state':'hecho', 'order_id': order_id})
            rec.message_post(
            body=_("%s Cambio al Estado \
             <b><em>Hecho</em></b>." % rec.sequence))
            # rec.message_post(
            # body=_("%s Genero la Compra \
            #  <b><em>%s</em></b>." % (rec.sequence, order_br.name)))
        return True

    def cancelar(self, cr, uid, ids, context=None):
        # self.write(cr, uid, ids, 
        #     {'state':'inscrito'}, context)
        for rec in self.browse(cr, uid, ids, context):
            rec.write({'state':'cancelado'})
            rec.message_post(
            body=_("%s Cambio al Estado \
             <b><em>Cancelado</em></b>." % rec.sequence))
        return True

    def nuevo(self, cr, uid, ids, context=None):
        # self.write(cr, uid, ids, 
        #     {'state':'inscrito'}, context)
        for rec in self.browse(cr, uid, ids, context):
            rec.write({'state':'nuevo'})
            rec.message_post(
            body=_("%s Cambio al Estado \
             <b><em>Nuevo Registro</em></b>." % rec.sequence))
        return True

    def copy(self, cr, uid, id, default=None, 
        context=None):
        # default = {} Diccionario con valores a poner
        # por defecto!!!
        secuencia_obj = self.pool.get('ir.sequence')
        sequence_id = secuencia_obj.search(
            cr, uid, [('code','=','project.home')])
        secuencia = secuencia_obj.get_id(cr, 
            uid, sequence_id[0])

        default.update({
            'sequence': secuencia,
            'order_id': False,
            'state': 'nuevo',
            })

        res = super(project_home, self).copy(
            cr, uid, id, default, context)
        return res



    def unlink(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids, context):
            if rec.state in ('confirmado','hecho'):
                raise osv.except_osv(
                    _('Error!'),
                    _('No puedes borrar un Registro\
                    que no esta en estado Nuevo'))
        res = super(project_home, self).unlink(
            cr, uid, ids, context)
        return res

    def create(self, cr, uid, vals, context=None):
        secuencia_obj = self.pool.get('ir.sequence')
        sequence_id = secuencia_obj.search(
            cr, uid, [('code','=','project.home')])
        secuencia = secuencia_obj.get_id(cr, 
            uid, sequence_id[0])
        vals.update({'sequence': secuencia})

        res = super(project_home, self).create(
            cr, uid, vals, context)
        return res

    _order = 'id desc' 