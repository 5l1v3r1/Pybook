import urllib
import threading
import time
import types
from parser import *
from helper import *




tsleep  = 0

def BasicMessageHook(session,text,_threading=0):
	if _threading == 0:
		threading.Thread(target=BasicMessageHook,args=(session,text,1,)).start()
	else:
		logger("Basic messages hook engine started")

		while 1:
			time.sleep(tsleep)
			msgs = GetUnreadOnly(session["session"])
			if len(msgs) > 0:
				for unread in msgs:
					send(session["session"],session["fb_dtsg"],text,unread)




def StaticMessageHook(session,options,replies={},_threading=0):

	if _threading == 0:
		"""
		Starting function thread
		"""
		threading.Thread(target=StaticMessageHook,args=(session,options,replies,1,)).start()
	else:
		
		logger("Dictionary messages hook engine started")

		# default options 
		doptions = {
			"keysearch"	: 0,
			"failReply"	: 0,
			"replyHook" : None
		}
		dreplies = {"failReply":""}

		dreplies.update(replies)
		doptions.update(options)

		# Messaging loop
		while (1):
			"""
			Have some sleep :D
			"""
			time.sleep(tsleep)

			for msg in ParseMessages(session["session"]):
				FailedToReply = 0
				if msg != None:
					if msg["status"] == "unread":
						if doptions["replyHook"] != None:
							reply = doptions["replyHook"](msg["last_message"])
							send(session["session"],session["fb_dtsg"],reply,msg["url"])
						else:
							try:
								if doptions["keysearch"] == 0:
									reply = dreplies[msg["last_message"]]
									if types.FunctionType == type(reply):
										reply = reply(msg["last_message"])
								else:
									reply = dreplies[FindInDict(msg["last_message"],dreplies,1)]
									if types.FunctionType == type(reply):
										reply = reply(msg["last_message"])
							except:
								FailedToReply = 1
								reply = dreplies["failReply"]
							if FailedToReply:
								if doptions["failReply"]:
									send(session["session"],session["fb_dtsg"],reply,msg["url"])
							else:
								send(session["session"],session["fb_dtsg"],reply,msg["url"])
								

						

							



def send(session,fb_dtsg,text,to):
    if text != "":
        logger("Replying to [{}]".format(to))

        data = {
            'fb_dtsg': urllib.unquote(str(fb_dtsg)).decode('utf8'),
            'body': text,
            'send': 'Send',
            'cver': 'legacy',
            'tids': urllib.unquote(to).decode('utf8'),
        }
    
        session.post('https://mbasic.facebook.com/messages/send/', data=data)


