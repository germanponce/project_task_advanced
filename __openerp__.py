# -*- coding: utf-8 -*-
#
#
{
    'name': "Presupuestos para Inmobiliarias",
    'description': """
Presupuestos para Inmobiliarias
===============================

Este modulo crea un menu con el cual podras crear Presupuestos para Empresas Inmobiliarias y poder generar un Pedido de Compra a partir de este.

Los Calculos son en base al total de Viviendas y cada linea de presupuesto es definida de forma unitaria.

Quedando total * numero de viviendas.

Al generar la orden de Compra, esta se creara de la siguiente manera:

cantidad de producto * numero de viviendas.



    """, # Descripcion
    'author': "Daniel Maraboli - Javier Herrera", # Autor
    'category': 'Sales', # Categoria / Empresa
    'version': '0.1', # 
    'depends': ["purchase","sale","account"], # Dependencias del Modulo
    'data': [
    
        'quotation.xml',

    ],
    'installable': True, 
    'auto_install': False,
}