# -*- coding: utf-8 -*-

{
    'name': "Generacion de Tareas en Base a Presupuestos",
    'description': """
Generacion de Tareas y Mejoras de Proyectos
===========================================

Este modulo permite generar una Tarea desde una linea de Presupuesto.

Al generar una tarea desde linea de Pedido esta creara una relacion entre ambas, si se elimina la tarea relacionada con la linea del presupuesto, podras crearla nuevamente, en caso contrario no te dejara hacerlo.

Al crear una tarea si no existe el proyecto lo creara, en caso contrario solo lo relacionara.

    """, # Descripcion
    'author': "German Ponce Dominguez", # Autor
    'category': 'Sales', # Categoria / Empresa
    'version': '0.1', # 
    'depends': ["purchase","sale","project","sale_crm","account_payment_sale","sale_commission","siur_customizations","analytic"], # Dependencias del Modulo
    'data': [
    
        'project.xml',
        'security/ir.model.access.csv',

    ],
    'installable': True, 
    'auto_install': False,
}