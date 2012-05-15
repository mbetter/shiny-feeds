Shiny Feeds is an XMPP (Jabber, GChat, etc) based microblogging platform All posting and editing 
is done through commands sent to an XMPP chat bot.

INSTALLING:

Copy settings.example.py to settings.py and modify appropriately. Run xmpp-listener.py, which 
does the actual XMPP work (you might need to open port 5222 in your router settings). Run 
shiny.py to use web.py debug web server or setup as a WSGI application.

USAGE: 

A shiny feeds command consists of a single character (case-insensitive) followed by a 
space-separated list of parameters. You only need to know a few commands to use shiny feeds effectively:

n <post title> - Creates a new post with a given title. The bot will reply with the id number of the new post.

w <post id> <post body> - Overwrites body of specific post to passed text.

a <post id> <post text> - Appends passed text as a new paragraph in body of specific post.

l <limit> - Lists <limit> last posts.

x <post id> - Deletes specific post.



