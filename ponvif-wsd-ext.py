#!/usr/bin/python2

import json, getopt, sys, settings
from WSDiscovery import WSDiscovery

def usage():
    print "\nThis is the usage function\n"
    print 'Usage: '+sys.argv[0]+' --timeout <timeout>'

def main():
	try:
		opts,args=getopt.getopt(sys.argv[1:],"t",['timeout='])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-t","--timeout"):
			settings.TIMEOUT = int(arg)

if __name__ == "__main__":
	main()
	wsd = WSDiscovery()
	wsd.start()
	ret = wsd.searchServices(timeout=settings.TIMEOUT)
	lst = []
	for service in ret:
		d = {}	
		types=','.join(str(v) for v in service.getTypes())
		if 'onvif.org' in types:
			d['epr']=service.getEPR()
			d['xaddr']=service.getXAddrs()[::-1]
			d['types']=types
			d['scopes']=','.join(str(v) for v in service.getScopes())
			lst.append(d)
	print json.dumps(lst)
	
	wsd.stop()

