#!/usr/bin/python2

# Python program that can send out M-SEARCH messages using SSDP (in server
# mode), or listen for SSDP messages (in client mode).

import sys, settings, json
from twisted.internet import reactor, task
from twisted.internet.protocol import DatagramProtocol
from urlparse import urlparse

catched=[]
lst=[]

class Base(DatagramProtocol):
    def datagramReceived(self, datagram, address):
	global catched
	data=datagram.rsplit('\r\n')
        for element in data:
		if 'LOCATION:' in element:
			xmllink=element.split('LOCATION:')[1].strip()
		elif 'Location:' in element:
			xmllink=element.split('Location:')[1].strip()
		elif 'USN:' in element:
			usn=element.split('USN:')[1].strip()
	ip=urlparse(xmllink).hostname
	if ip not in catched:
		catched.append(ip)
		d = {}
		d['ip']=ip
		d['location']=xmllink
		d['usn']=usn
		lst.append(d)
		#print json.dumps(d)
	'''
	else:
		print 'ignoring %s' % ip
	'''
        '''
	first_line = datagram.rsplit('\r\n')[0]
        print "Received %s from %r" % (first_line, address, )
	print datagram
        '''

    def stop(self):
        pass

class Server(Base):
    def __init__(self, iface):
        self.iface = iface
        task.LoopingCall(self.send_MSearch).start(6) # every 6th seconds
	reactor.callLater(settings.SSDP_TIMEOUT,self.blockMeNow)

    def blockMeNow(self):
	global lst
	print json.dumps(lst)
	reactor.fireSystemEvent('shutdown')

    def send_MSearch(self):
        port = reactor.listenUDP(0, self, interface=self.iface)
        # print "Sending M-SEARCH..."
        port.write(settings.MS, (settings.SSDP_ADDR, settings.SSDP_PORT))
        reactor.callLater(2.5, port.stopListening) # MX + a wait margin

class Client(Base):
    def __init__(self, iface):
        self.iface = iface
        self.ssdp = reactor.listenMulticast(settings.SSDP_PORT, self, listenMultiple=True)
        self.ssdp.setLoopbackMode(1)
        self.ssdp.joinGroup(settings.SSDP_ADDR, interface=iface)

    def stop(self):
        self.ssdp.leaveGroup(settings.SSDP_ADDR, interface=self.iface)
        self.ssdp.stopListening()

def main(mode, iface):
    klass = Server if mode == 'server' else Client
    obj = klass(iface)
    reactor.addSystemEventTrigger('before', 'shutdown', obj.stop)

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) >4:
        print "Usage: %s <server|client> <IP of interface> <timeout>" % (sys.argv[0], )
        sys.exit(1)
    mode=sys.argv[1]
    iface = sys.argv[2]
    if len(sys.argv)==4:
	settings.SSDP_TIMEOUT=int(sys.argv[3])
    reactor.callWhenRunning(main, mode, iface)
    reactor.run()
   
