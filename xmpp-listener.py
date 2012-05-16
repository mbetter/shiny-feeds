#!/usr/bin/python
import web
import sys
import logging
import sleekxmpp
import settings

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input

def onterm(signum, frame):
    print 'Received signal %s' % signum
    os.remove(config.proc['pidfile'])
    sys.exit(0)

class PostBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, user, database):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.db = database
        self.user = user
    def start(self, event):
        self.send_presence()
        self.get_roster()
    def parse_message(self, msg, user_record):
        tokens = msg['body'].partition(" ")
        cmd = tokens[0].lower()
        user_jid = msg['from'].jid.partition('/')[0]
        current = user_record.current_post
        page_name = user_record.page
 
        if cmd == "n":
            n = self.db.insert('posts', title=tokens[2], page=page_name)
            self.db.update('users', where="jid = '%s'" % user_jid, current_post = n)
            msg.reply('Added post #%d.' % n).send()
        elif cmd == "t":
            params = tokens[2].partition(" ")
            try:
                i = int(params[0])
                if db.update('posts', where="id = %s" % i, title=params[2]):
                    msg.reply('Updated post #%d.' % i).send()
                else:
                    msg.reply('Post #%d not found.' % i).send()
            except ValueError:
                msg.reply('Invalid post id.').send()
        elif cmd == "w":
            params = tokens[2].partition(" ")
            try:
                i = int(params[0])
                post = db.select('posts', where="id = %s" % i)
                if db.update('posts', where="id = %s" % i, post=params[2]):
                    msg.reply('Updated post #%d.' % i).send()
                else:
                    msg.reply('Post #%d not found.' % i).send()
            except ValueError:
                msg.reply('Invalid post id.').send()
        elif cmd == ">":
		p = db.select('posts',where='id = %d' % current).list()
		if p:
		    db.update('posts', where="id = %d" % current, post=p[0].post + '\n\n' + tokens[2])
		    msg.reply('Updated post #%d.' % current).send()
		else:
		    msg.reply('Post #%d not found.' % current).send()
        elif cmd == "\\":
		p = db.select('posts',where='id = %d' % current).list()
		if p:
		    db.update('posts', where="id = %d" % current, post=p[0].post + '\n' + tokens[2])
		    msg.reply('Updated post #%d.' % current).send()
		else:
		    msg.reply('Post #%d not found.' % current).send()
        elif cmd == "a":
            params = tokens[2].partition(" ")
            try:
                i = int(params[0])
                p = db.select('posts',where='id = %s' % i).list()
                if p:
                    db.update('posts', where="id = %s" % i, post=p[0].post + '\n\n' + params[2])
                    msg.reply('Updated post #%d.' % i).send()
                else:
                    msg.reply('Post #%d not found.' % i).send()
            except ValueError:
                msg.reply('Invalid post id.').send()
        elif cmd == "l":
            params = tokens[2].partition(" ")
            try:
                i = int(params[0])
                limit = i
            except ValueError:
                limit = 10
            p = db.select('posts',order="time DESC",limit=limit)
            for postrow in p:
                self.send_message(mto=msg['from'],
                                  mbody='%d: %s.' % (postrow.id, postrow.title),
                                  mtype='chat')
            self.send_message(mto=msg['from'],
                              mbody='End of list.',
                              mtype='chat')
        elif cmd == "x":
            params = tokens[2].partition(" ")
            try:
                i = int(params[0])
                if db.delete('posts', where="id = %s" % i):
                    msg.reply('Deleted post #%d.' % i).send()
                else:
                    msg.reply('Post #%d not found.' % i).send()
            except ValueError:
                msg.reply('Invalid post id.').send()


    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            # print(msg['from'].jid)
            # print(msg['from'].jid.partition('/')[0] in self.user)
            user_jid = msg['from'].jid.partition('/')[0]
            user_dbrow = self.db.select('users',where="jid ='%s'" % user_jid).list()
            if user_dbrow:
                user_record = user_dbrow[0]
            else:
                self.db.insert('users', jid=user_jid, current_post=0, page=user_jid)
                user_record.jid = user_jid
                user_record.current_post=0
                user_record.page = user_jid
            print(msg['body']) 
            print(user_record.page)
            self.parse_message(msg,user_record)


db = web.database(host=settings.db_host, dbn=settings.db_dbn, user=settings.db_user, pw=settings.db_password, db=settings.db_database)

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, format='%(levelname)-8s %(message)s')
    xmpp = PostBot(settings.xmpp_jid, settings.xmpp_pw, settings.xmpp_user, db)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199') # XMPP Ping
    if xmpp.connect():
        xmpp.process(block=True)
    	sys.exit(0)
    else:
        print("Unable to connect.")

