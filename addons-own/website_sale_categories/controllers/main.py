# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request

from openerp.addons.website_sale.controllers import main

# import the base controller class to inherit from
from openerp.addons.website_sale.controllers.main import website_sale


class website_sale_categories(website_sale):

    @http.route()
    def shop(self, page=0, category=None, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        # Try to set product grid before the Controller get's started
        if category:
            category = pool['product.public.category'].browse(cr, uid, int(category), context=context)
            # HINT: If the category has not Parent the cat_root_id will be the category itself
            main.PPG = 9
            main.PPR = 3

        return super(website_sale_categories, self).shop(page=page, category=category, search=search, **post)

    # List only products in the same cat_root_id tree:
    def _get_search_domain(self, search, category, attrib_values):
        domain = super(website_sale_categories, self)._get_search_domain(search, category, attrib_values)
        category_obj = request.registry['product.public.category']
        if category:
            # 1.) Find all relevant categories (self, and children with the same cat_root_id)
            #     HINT: child_of operator will find self and children! (so not only children as maybe expected)
            child_categories = category_obj.search(request.cr, request.uid,
                                                   ['&',
                                                    ('parent_id', 'child_of', int(category)),
                                                    ('cat_root_id', '=', int(category.cat_root_id))],
                                                   context=request.context)
            # 2.) Extend the product search domain to only show products which are in one or more of the categories
            domain += [('public_categ_ids', 'in', child_categories)]
        else:
            # Only search in non root categories:
            # if a product has no public_categ_ids
            # if a product is in one or more public (non root) categories
            nonroot_categories = category_obj.search(request.cr, request.uid,
                                                     [('cat_root_id.cat_root', '=', False)],
                                                     context=request.context)
            domain += ['|', ('public_categ_ids', '=', False), ('public_categ_ids', 'in', nonroot_categories)]
        return domain

