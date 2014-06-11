ponvif_ext
==========

PONVIF Discovery Extensions 1.0

**** How use discovery module in your PHP code:

1) Required module (for WS and UPNP) 

   require "lib/class.ponvif_ext.php";

2) WS Discovery: 

    try { 
        $test=new ponvif_ext();
        $results=$test->wsdiscovery();
        ....
    } catch (Exception $e) {
      ....
    }

2.1) Collateral functions:

2.1.a) setWSDiscoveryScriptPath($scriptPath): use this if you need to change the pointing to the Python script ponvif-wsd-ext.py

2.1.b) setWSDTimeout($timeout): use this to change the default timeout (how long the WS Discovery module have to wait before end); value in seconds; default is 5

2.1.c) getWSDTimeout(): get current WS Discovery timeout

3) UPNP Discovery:

    try { 
        $test=new ponvif_ext();
        ...
        $checkIfOnvif=true; // if true, tries to check if camera is ONVIF compliant (default is false)
        ...
        $filters=array(); // if empty, finds all UPNP devices (default is empty)
        ...
        $filters=array('ModelName'=>'camera','ModelDescription'=>'camera'); // if defined, tries to find a specific type of devices (in this case cameras)
        ... 
        $results=$test->upnpdiscovery($checkIfOnvif, $filters);
        ....
    } catch (Exception $e) {
      ....
    }
 
3.1) Collateral functions:

3.1.a) setUPNPDiscoveryScriptPath($scriptPath): use this if you need to change the pointing to the Python script ponvif-upnp-ext.py

3.1.b) setUPNPTimeout($timeout): use this to change the default timeout (how long the UPNP discovery module have to wait before end); value in seconds; default is 5

3.1.c) getUPNPTimeout(): get current UPNP discovery timeout

3.1.d) setUPNPInspectTimeout($timeout): use this to change the default timeout (connection timeout used during details acquisition and onvif compatibility checking); value in seconds; default is 10

3.1.e) getUPNPInspectTimeout(): get current UPNP discovery inspection timeout

3.1.f) setUPNPIface($iface): change the local IPv4 or IPv6 address to which to bind

3.1.g) getUPNPIface(): get current interface setting

**** Dependencies

1) Discovery's extensions are based on Python scripts. Scritps invoked by PHP are:

      ponvif-upnp-ext.py
      ponvif-wsd-ext.py
      settings.py
      WSDiscovery.py
      
   Please don't remove and leave all them at the same folder level of your PHP invoking module.

2) Required Python extensions:

     python-twisted
     python-netifaces
     python-minimal
     python-configglue

3) Required PHP extensions:

     php5-curl

**** Compatibility Test

Tested with python 2.7.3, Twisted 11.

Tested with PHP 5.3.10, Curl 7.22.0.
