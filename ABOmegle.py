#!/usr/bin/python
"""
introduce a bot running through Program-AB to an Omegle user (or another bot)

logs conversations locally to bots/<BOTNAME>/logs

"""
import urllib2 as url
import urllib
import httplib as http
import pexpect, json, requests, time, random, sys, os

_LOGGING = True # set to false if you don't  want to log
_BOT = "alice" # name of bot in bots directory
_TRACE = "false" # print trace or not - not yet working - let me know if you want this feature or have implemented it
_LAST_LOG = ''

def log_line(fName, line):
    if _LOGGING:
        try:
            fPath = os.path.join(os.getcwd(), 'bots', _BOT, 'logs', fName)
            with open(fPath, 'ab') as lf:
                lf.write(line+'\n')
                lf.close()
        except Exception, ex:
            print "ERROR:\nfailed to log line:"
            print ex

def set_last_log():
    """
    sets _LAST_LOG to the name of the last conversation log file, which is a string of
    numbers and is used to make the name of the next (this) log file by incrementing it by 1
    """
    global _LAST_LOG

    def isInt(s):
        """ true if s is a numerical string"""
        try: 
            int(s)
            return True
        except ValueError:
            return False

    # list of ints from filenames found in the bots logs dir that can be represented as a number
    logfiles = [int(f) for f in os.listdir(os.path.join(os.getcwd(), 'bots', _BOT, 'logs')) if isInt(f)]
    if len(logfiles) == 0:
        _LAST_LOG = '0'
        return True
    logfiles.sort()
    _LAST_LOG = str(logfiles[-1])

def start_convo():
	"""
	returns a child process to talk to
	"""
	return pexpect.spawn('java -cp lib/Ab.jar Main action=chat bot={} trace={}'.format(_BOT, _TRACE))

#This simply cuts the extra characters to isolate the ID
def fmtId( s ):
    return s[1:len( s ) - 1]

#Talk to people
def talk(id,req,hMsg,cp):

    #Show the server that we're typing
    typing = url.urlopen('http://omegle.com/typing', '&id='+id)
    typing.close()

    # get it from the bot
    # msg = get_response(human_input=hMsg)
    ##############################
    cp.expect("Human:")
    cp.sendline(hMsg+'\n')
    cp.expect("Robot:")
    cp.expect("Human:")
    msg = cp.before
    msg = msg.strip().replace('\n', '')
    ##############################
    time.sleep(random.randint(1, 3))
    log_line(fName=_LAST_LOG, line="Robot: "+msg)
    print "Robot:", msg

    #Send the string to the stranger ID
    msgReq = url.urlopen('http://omegle.com/send', '&msg='+msg+'&id='+id)

    #Close the connection
    msgReq.close()


#This is where all the magic happens, we listen constantly to the page for events
def listenServer( id, req, cp ):

    while True:

        site = url.urlopen(req)

        #We read the HTTP output to get what's going on
        rec = site.read()

        connected = True

        if 'waiting' in rec:
            print("Looking for humans ...")

        elif 'connected' in rec and connected:
            # double connection thing. treat as dc
            print('Human has left')
            #We start the whole process again
            omegleConnect()

        elif 'connected' in rec:
            print('Found one')
            print(id)
            if 'gotMessage' in rec:
                humanMsg = rec[16:len( rec ) - 2]
                print "Human:", humanMsg
                log_line(fName=_LAST_LOG, line="Human: "+humanMsg.strip())
                talk(id,req,humanMsg,cp)
            else:
                print "!! WEIRD EDGE CASE FOR SOME REASON !!"
                talk(id,req,"",cp)
            
        elif 'strangerDisconnected' in rec:
            print('Human has left')
            # disconnect the bot
            # change to wq if we want to save
            cp.sendline("q\n")
            #We start the whole process again
            omegleConnect()
            
        elif 'typing' in rec:
            print("Human is typing something...")

        #When we receive a message, print it and execute the talk function            
        elif 'gotMessage' in rec:
            humanMsg = rec[16:len( rec ) - 2]
            print "Human:", humanMsg
            log_line(fName=_LAST_LOG, line="Human: "+humanMsg.strip())
            talk(id,req,humanMsg,cp)


#Here we listen to the start page to acquire the ID, then we "clean" the string to isolate the ID
def omegleConnect():
    global _LAST_LOG
    id = ''
    while id == '':
        site = url.urlopen('http://omegle.com/start','')    
        id = fmtId( site.read() )
        if id == '' or id == None:
            print "no shard, trying again.."
            id = ''
            time.sleep(2.5)
            continue
        # print(id)
        req = url.Request('http://omegle.com/events', urllib.urlencode( {'id':id}))
        
        print "starting conversation with", _BOT, "..."

        # start a conversation
        c = start_convo()
        print "started a new conversation with", _BOT

        # increment _LAST_LOG
        _LAST_LOG = str(int(_LAST_LOG)+1)

        #Then we open our ears to the wonders of the events page, where we know if anything happens
        #We have to pass two arguments: the ID and the events page.
        listenServer(id,req,c)

set_last_log()
omegleConnect()