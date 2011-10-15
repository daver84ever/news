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

class NewsHandler(webapp.RequestHandler):
    def get(self):
        query = News.all()
        query.order("-createdAt")
        results = query.fetch(limit=50)

        #if results is None:
        #    results = News()
        self.response.out.write("<b>ID HEADLINE CONTENT DATE</b><br>")
        
        for news in results:
            self.response.out.write('%s  <i><b>%s</b></i>  %s  %s' % ( str(news.newsId), news.headline, news.content, str(news.createdAt) ) )
            self.response.out.write('<a href="http://www.eppyfong.appspot.com/delete/%s">        <i>(delete)</i></a><br>' % news.key())

class DeleteNewsHandler(webapp.RequestHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        self.response.out.write(resource)

        self.response.out.write("\n <h2>I've been thinking about this .... and you shouldnt delete the news! I mean that's history man......;(</h2>")
        #_news = News.get(resource)
        #_news.delete()
        #self.redirect('/news')

class GetNewsHandler(webapp.RequestHandler):
    def get(self):
        out = todaysNews()
        self.response.out.write(out)

    def post(self):
        out = todaysNews()
        self.response.out.write(out) 

def todaysNews():
    query = News.all()
    query.order("-createdAt")
    results = query.fetch(limit=1)

    mostRecentNews = results.pop()

    # Create the minidom level document
    doc = Document()
    newsElement = doc.createElement("news")
    doc.appendChild(newsElement)

    #headline
    headlineElement = doc.createElement("headline")
    headline = doc.createTextNode(mostRecentNews.headline)
    headlineElement.appendChild(headline)
    newsElement.appendChild(headlineElement)

    #content
    contentElement = doc.createElement("content")
    content = doc.createTextNode(mostRecentNews.content)
    contentElement.appendChild(content)
    newsElement.appendChild(contentElement)

    #date
    dateElement = doc.createElement("date")
    date = doc.createTextNode(str(mostRecentNews.createdAt))
    dateElement.appendChild(date)
    newsElement.appendChild(dateElement)

    out = doc.toxml()
    return out
            
        

class LoadNewsHandler(webapp.RequestHandler):
    def post(self):
        _headline = self.request.get("headline")
        _content = self.request.get("content")

        query = News.all()
        count = query.count()
        
        news = News()
        news.headline =str(_headline)
        news.content = str(_content)
        news.newsId = count
        news.put()
        #self.response.out.write(_headline)
        #self.response.out.write(_content)
        self.redirect('/news')
    
class LoadNewsFormHandler(webapp.RequestHandler):
    def get(self):
        upload_url = '/newsloader' #blobstore.create_upload_url('/upload')
        self.response.out.write('<html><body>')
        self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url )
        self.response.out.write("""Upload News:<br> <b>HEADLINE</b><input type="text" name="headline"><br> <b><i>story:</i><b/><br>
                                <TEXTAREA name="content" rows="20" cols="80"></TEXTAREA><br>
                                <input type="submit" name="submit" value="Submit"> </form></body></html>""")
