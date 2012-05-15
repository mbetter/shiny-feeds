#!/usr/bin/python
import web
import sys
import os
import logging
import sleekxmpp
import markdown

curdir = os.path.dirname(__file__)
sys.path.insert(0, curdir)

import settings

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input

t_globals = {
    'markdown': markdown.markdown,
}
render = web.template.render(os.path.join(curdir,'templates'), globals=t_globals)

db = web.database(host=settings.db_host, dbn=settings.db_dbn, user=settings.db_user, pw=settings.db_password, db=settings.db_database)

urls = (
    '/', 'index'
)

class index:
    def GET(self):
        todos = db.select('posts')
        return render.index(todos)

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()

