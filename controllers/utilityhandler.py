#!/usr/bin/env python
__author__ = 'daver'

import os
import os.path
import datetime
import urllib
import logging
import wsgiref.handlers

from models.newsmodel import *

from datetime import timedelta
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from xml.dom import minidom
from xml.dom.minidom import getDOMImplementation
from xml.dom.minidom import Document

class UtilityHandler(webapp.RequestHandler):
    def get(self):
        temp = os.path.join(os.path.dirname(__file__),'../templates/utility.htm')
        outStr = template.render(temp,{})
        self.response.out.write(outStr)
