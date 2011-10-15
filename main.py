#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import os.path

from controllers import newshandler
from controllers import utilityhandler

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


class MainHandler(webapp.RequestHandler):
    def get(self):
        #self.response.out.write('Hello Alex! Why dont you go to /loadnewsform')
        temp = os.path.join(os.path.dirname(__file__),'templates/hello.htm')
        outStr = template.render(temp,{'name' : 'Alex'})
        self.response.out.write(outStr)

def main():
    application = webapp.WSGIApplication(
        [('/', MainHandler),
        (r"/newsloader", newshandler.LoadNewsHandler),
        (r"/loadnewsform", newshandler.LoadNewsFormHandler),
        (r"/news", newshandler.NewsHandler),
        (r"/getnews", newshandler.GetNewsHandler),
        (r"/delete/(.*)", newshandler.DeleteNewsHandler),
        (r"/speed", utilityhandler.UtilityHandler),
        ],debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
