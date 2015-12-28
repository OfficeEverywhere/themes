# -*- coding: utf-8 -*-
import cStringIO
import datetime
from itertools import islice
import json
import xml.etree.ElementTree as ET

import logging
import re

import werkzeug.utils
import urllib2
import werkzeug.wrappers
from PIL import Image

import openerp
from openerp.addons.web.controllers.main import WebClient
from openerp.addons.web import http
from openerp.http import request, STATIC_CACHE
from openerp.tools import image_save_for_web

logger = logging.getLogger(__name__)

# Completely arbitrary limits
MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT = IMAGE_LIMITS = (1024, 768)
LOC_PER_SITEMAP = 45000
SITEMAP_CACHE_TIME = datetime.timedelta(hours=12)

class Website(openerp.addons.web.controllers.main.Home):

    #------------------------------------------------------
    # bootswatch change
    #------------------------------------------------------

    @http.route('/theme_bootswatch_native/bootswatch_change', type='http', auth="user", website=True)
    def bootswatch_change(self, theme_id=False, **kwargs):
        imd = request.registry['ir.model.data']
        Views = request.registry['ir.ui.view']

        _, theme_template_id = imd.get_object_reference(
            request.cr, request.uid, 'website', 'theme')
        views = Views.search(request.cr, request.uid, [
            ('inherit_id', '=', theme_template_id),
        ], context=request.context)
        Views.write(request.cr, request.uid, views, {
            'active': False,
        }, context=dict(request.context or {}, active_test=True))

        if theme_id:
            module, xml_id = theme_id.split('.')
            _, view_id = imd.get_object_reference(
                request.cr, request.uid, module, xml_id)
            Views.write(request.cr, request.uid, [view_id], {
                'active': True
            }, context=dict(request.context or {}, active_test=True))

        return request.render('website.bootswatch', {'bootswatch_changed': True})
