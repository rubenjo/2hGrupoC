# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import api, fields, models, _
from openerp.exceptions import UserError
import calendar
import datetime
from datetime import date, timedelta
import time

class Hrinfraestructuras(models.Model):

    _name = "hr.infraestructuras"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "Infraestructuras"
    _order = "name"
    
    #Campos para el formulario de misiones/viajes
    
    name = fields.Char(string='Descripción', required=True, size=255)
    x_solicitante = fields.Char(string='Solicitante', required=True)
    instalaciones2 = fields.Many2many('hr.infraestructuras.instalaciones', string='Instalaciones', required=True, store=True)
    
    x_fecha_inicio = fields.Date(string="Fecha de inicio", required=True)
    x_fecha_fin = fields.Date(string="Fecha de fin", required=True)
    x_duracion_dias = fields.Integer(string="Nº de días", store=True)
    
    x_hora_inicio = fields.Float(string="Hora de inicio", required=True, store=True)
    x_hora_fin = fields.Float(string="Hora de fin", required=True, store=True)
    x_duracion_horas = fields.Float(string="Duración", readonly=True, compute="_hora_change", store=True)
    
    x_asistentes = fields.Char(string='Número de asistentes previstos', required=True)
    x_requerimientos = fields.Many2many('hr.infraestructuras.requerimientos', string='Requerimientos')
    
    x_correo = fields.Char(string='Email', required=True)
    x_telefono = fields.Char(string='Teléfono', required=True)
    x_institucion = fields.Char(string='Institución', required=True)
    
    x_adjunto = fields.Integer(compute='_compute_attachment_number', string='Nº de adjuntos')
    x_observaciones = fields.Text(string="Observaciones")
    #Probando a añadir timesheets a helpdesk
    timesheet_ids = fields.One2many('account.analytic.line', 'cesion_infraestructuras', string="Timesheets")    
    analytic_account_id = fields.Integer(string="Analytic Account", compute="_compute_analytic")

    @api.multi
    def _compute_analytic(self):
        aux1 = self.name
        aux2 = self.env['account.analytic.account'].search([('name', '=', aux1)]).id
        self.analytic_account_id = aux2
        
#Para crear en account.analytic.account la categoria del correo de help desk
    @api.model
    def create(self, values):
        # here we call to the parent create method
        res = super(Hrinfraestructuras, self).create(values)
        
        # here we create a record in the demo model
        # and we can access to the values of the current model
        self.env['account.analytic.account'].create({
            'name': values['name'],
            'account_type': 'normal'
        })

        return res
    
    @api.multi
    def _compute_attachment_number(self):
        attachment_data = self.env['ir.attachment'].read_group([('res_model', '=', 'hr.infraestructuras'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for infra in self:
            infra.x_adjunto = attachment.get(infra.id, 0)
            
    @api.multi
    def action_get_attachment_view(self):
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('base', 'action_attachment')
        res['domain'] = [('res_model', '=', 'hr.infraestructuras'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'hr.infraestructuras', 'default_res_id': self.id}
        return res
    
    #@api.depends('x_fecha_inicio','x_fecha_fin')       
    #@api.multi
    #def _fecha_change(self):
    #    if self.x_fecha_fin and self.x_fecha_inicio:
    #        fmt = '%Y-%m-%d'
    #        d1 = datetime.datetime.strptime(self.x_fecha_inicio, fmt)
    #        d1 = datetime.datetime.strptime(self.x_fecha_inicio, fmt)
    #        d2 = datetime.datetime.strptime(self.x_fecha_fin, fmt)
    #        timedelta = d2 - d1
    #        diff_day = timedelta.days + float(timedelta.seconds) / 86400
    #        if self.x_fecha_fin > self.x_fecha_inicio:
    #            self.x_duracion_dias = diff_day+1
    #        else:
    #            self.x_duracion_dias = 1
    
    @api.depends('x_hora_inicio','x_hora_fin')            
    @api.multi
    def _hora_change(self):
        if self.x_hora_fin and self.x_hora_inicio:
            if self.x_hora_fin > self.x_hora_inicio:
                aux = self.x_hora_fin - self.x_hora_inicio
                self.x_duracion_horas = aux
            else:
                self.x_duracion_horas = 0
    
class Hrinfraestructuras_instalaciones(models.Model):
    _name = 'hr.infraestructuras.instalaciones'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "Instalaciones"
    _order = "name desc"
    
    name = fields.Char(string='Instalación', required=True)
    
    

class Hrinfraestructuras_requerimientos(models.Model):
    _name = 'hr.infraestructuras.requerimientos'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "Requerimientos"
    _order = "name desc"
    
    name = fields.Char(string='Requerimiento', required=True)
    
    
class account_analytic_line(models.Model):
    _inherit = "account.analytic.line"
    
    cesion_infraestructuras = fields.Many2one('hr.infraestructuras', string="Cesión de infraestructura")
    
    
    
    

