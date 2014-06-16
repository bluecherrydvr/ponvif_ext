#!/usr/bin/python2

# Super fast WS-Discovery using twisted. Buona idea per implementazione snella. 

# Python program that can send out PROBE messages using WS-Discovery (in server
# mode), or listen for WS-Discovery messages (in client mode).

import sys
from twisted.internet import reactor, task
from twisted.internet.protocol import DatagramProtocol

SSDP_ADDR = '239.255.255.250'
SSDP_PORT = 3702

# Specific for NVT (only onvif compliant)
# MS='<s:Envelope xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:d="http://schemas.xmlsoap.org/ws/2005/04/discovery" xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:dn="http://www.onvif.org/ver10/network/wsdl"><s:Header><a:Action>http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</a:Action><a:MessageID>uuid:fa8ce1d0-c4ed-0131-d962-0800272269d9</a:MessageID><a:To>urn:schemas-xmlsoap-org:ws:2005:04:discovery</a:To></s:Header><s:Body><d:Probe><d:Types>dn:NetworkVideoTransmitter</d:Types><d:Scopes/></d:Probe></s:Body></s:Envelope>'

# Generic for any device (including onvif compliant)
MS='<s:Envelope xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:d="http://schemas.xmlsoap.org/ws/2005/04/discovery" xmlns:s="http://www.w3.org/2003/05/soap-envelope"><s:Header><a:Action>http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</a:Action><a:MessageID>uuid:f7831e60-c4ed-0131-d962-0800272269d9</a:MessageID><a:To>urn:schemas-xmlsoap-org:ws:2005:04:discovery</a:To></s:Header><s:Body><d:Probe><d:Types/><d:Scopes/></d:Probe></s:Body></s:Envelope>'

class Base(DatagramProtocol):
    def datagramReceived(self, datagram, address):
        first_line = datagram.rsplit('\r\n')[0]
        print "Received %s from %r" % (first_line, address, )
	print datagram

    def stop(self):
        pass

class Server(Base):
    def __init__(self, iface):
        self.iface = iface
        task.LoopingCall(self.send_msearch).start(6) # every 6th seconds

    def send_msearch(self):
        port = reactor.listenUDP(0, self, interface=self.iface)
        print "Sending Probe..."
        port.write(MS, (SSDP_ADDR, SSDP_PORT))
        reactor.callLater(2.5, port.stopListening) # MX + a wait margin

class Client(Base):
    def __init__(self, iface):
        self.iface = iface
        self.ssdp = reactor.listenMulticast(SSDP_PORT, self, listenMultiple=True)
        self.ssdp.setLoopbackMode(1)
        self.ssdp.joinGroup(SSDP_ADDR, interface=iface)

    def stop(self):
        self.ssdp.leaveGroup(SSDP_ADDR, interface=self.iface)
        self.ssdp.stopListening()

def main(mode, iface):
    klass = Server if mode == 'server' else Client
    obj = klass(iface)
    reactor.addSystemEventTrigger('before', 'shutdown', obj.stop)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: %s <server|client> <IP of interface>" % (sys.argv[0], )
        sys.exit(1)
    mode, iface = sys.argv[1:]
    reactor.callWhenRunning(main, mode, iface)
    reactor.run()

