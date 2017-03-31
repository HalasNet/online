# -*- coding: utf-'8' "-*-"
import logging
from openerp import api, models, fields
from openerp import http

logger = logging.getLogger(__name__)


class WebsiteDomainManager(models.Model):
    _name = 'website.website_domains'
    _description = 'Website Domain Manager'

    domain = fields.Char(string='Domain', required=True, translate=True, help='E.g.: spenden.test.at')
    template = fields.Many2one(comodel_name='ir.ui.view', string="Domain Template",
                               domain=['&', ('type', '=', 'qweb'),
                                       ('model_data_id.name', '=like', '%website_domain_template%')])
    redirect_url = fields.Char(string='Redirect URL', translate=True, help='E.g.: https://www.test.at/de/shop')

    _sql_constraints = [('domain_uniq', 'unique (domain)', 'The domain must be unique!')]
