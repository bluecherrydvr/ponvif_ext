################################# UPNP Discovery (SSDP)
SSDP_ADDR = '239.255.255.250'
SSDP_PORT = 1900 # SSDP uses UDP transport on port 1900
SSDP_TIMEOUT = 10 # how long (seconds) should I wait for response before stop
MS = 'M-SEARCH * HTTP/1.1\r\nHOST: %s:%d\r\nMAN: "ssdp:discover"\r\nMX: 2\r\nST: ssdp:all\r\n\r\n' % (SSDP_ADDR, SSDP_PORT)



################################# WSDiscovery
TIMEOUT=10 # how long (seconds) should I wait for response before stop

# The WS-Discovery protocol uses SOAP and UDP (User Datagram Protocol) multicast to enable services 
# to be discovered by a client.
# The multicast address used is 239.255.255.250 on IPV4 networks. Multicast messages are sent to port 3702.
MULTICAST_PORT = 3702 
MULTICAST_IPV4_ADDRESS = "239.255.255.250"

# Please, change following settings only if you know what are you doing.
# Sockets
BUFFER_SIZE = 0xffff
APP_MAX_DELAY = 500 # milliseconds
_NETWORK_ADDRESSES_CHECK_TIMEOUT = 5
UNICAST_UDP_REPEAT=2
UNICAST_UDP_MIN_DELAY=50
UNICAST_UDP_MAX_DELAY=250
UNICAST_UDP_UPPER_DELAY=500
MULTICAST_UDP_REPEAT=4
MULTICAST_UDP_MIN_DELAY=50
MULTICAST_UDP_MAX_DELAY=250
MULTICAST_UDP_UPPER_DELAY=500

# SOAP
NS_A = "http://schemas.xmlsoap.org/ws/2004/08/addressing"
NS_D = "http://schemas.xmlsoap.org/ws/2005/04/discovery"
NS_S = "http://www.w3.org/2003/05/soap-envelope"

ACTION_HELLO = "http://schemas.xmlsoap.org/ws/2005/04/discovery/Hello"
ACTION_BYE = "http://schemas.xmlsoap.org/ws/2005/04/discovery/Bye"
ACTION_PROBE = "http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe"
ACTION_PROBE_MATCH = "http://schemas.xmlsoap.org/ws/2005/04/discovery/ProbeMatches"
ACTION_RESOLVE = "http://schemas.xmlsoap.org/ws/2005/04/discovery/Resolve"
ACTION_RESOLVE_MATCH = "http://schemas.xmlsoap.org/ws/2005/04/discovery/ResolveMatches"

ADDRESS_ALL = "urn:schemas-xmlsoap-org:ws:2005:04:discovery"
ADDRESS_UNKNOWN = "http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous"

MATCH_BY_LDAP = "http://schemas.xmlsoap.org/ws/2005/04/discovery/ldap"
MATCH_BY_URI = "http://schemas.xmlsoap.org/ws/2005/04/discovery/rfc2396"
MATCH_BY_UUID = "http://schemas.xmlsoap.org/ws/2005/04/discovery/uuid"
MATCH_BY_STRCMP = "http://schemas.xmlsoap.org/ws/2005/04/discovery/strcmp0"
