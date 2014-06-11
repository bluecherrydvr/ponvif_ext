<?php

define ('SCOPES_TYPE_REG','/,?onvif:\/\/www\.onvif\.org\/type\/([a-zA-Z0-9_.-\s;:\+\*]*)\,?/i');
define ('SCOPES_NAME_REG','/,?onvif:\/\/www\.onvif\.org\/name\/([a-zA-Z0-9_.-\s;:\+\*]*)\,?/i');
define ('SCOPES_LOCATION_REG','/,?onvif:\/\/www\.onvif\.org\/location\/([a-zA-Z0-9_.-\s;:\+\*]*)\,?/i');
define ('SCOPES_HARDWARE_REG','/,?onvif:\/\/www\.onvif\.org\/hardware\/([a-zA-Z0-9_.-\s;:\+\*]*)\,?/i');
define ('TYPES_NETWORK_REG','/,?http:\/\/www\.onvif\.org\/ver[0-9]+\/network\/[a-zA-Z]*:([a-zA-Z0-9_.-\s;:\+\*]*)\,?/i');
define ('TIMEOUT_DEFAULT',5);
define ('TIMEOUT_DEFAULT_UPNP',5);
define ('IFACE_DEFAULT_UPNP','0');
define ('DEVICE_TAG_UPNP_REG','/<%%TAG%%>(.*)<\/%%TAG%%>/');
define ('CHECKONVIF_UPNP_URL','http://%%IP%%:80/onvif/device_service');
define ('TIMEOUT_DEFAULT_INSPECT_UPNP', 10);

class ponvif_ext {

	// WSDiscovery
	protected $wsdscript;
	protected $timeout;
	protected $re_scopes=array();
	protected $re_type=array();
	protected $re_device_upnp=array();

	// UPNP  Discovery
	protected $upnpdscript;
	protected $upnptimeout;
	protected $upnpiface;
	protected $upnptimeoutinspect;

	/*
                Properties wrappers
        */
        public function setWSDiscoveryScriptPath($scriptPath) { $this->wsdscript = $scriptPath; }
	public function setWSDTimeout($timeout) { $this->timeout=$timeout; }
	public function getWSDTimeout() { return $this->timeout; }
        public function setUPNPDiscoveryScriptPath($scriptPath) { $this->upnpdscript = $scriptPath; }
	public function setUPNPTimeout($timeout) { $this->upnptimeout=$timeout; }
	public function getUPNPTimeout() { return $this->upnptimeout; }
	public function setUPNPInspectTimeout($timeout) { $this->upnptimeoutinspect=$timeout; }
	public function getUPNPInspectTimeout() { return $this->upnptimeoutinspect; }
	public function setUPNPIface($iface) { $this->upnpiface=$iface; }
	public function getUPNPIface() { return $this->upnpiface; }

        /*
                Constructor & Destructor
        */
        public function __construct()
        {
		$this->timeout=TIMEOUT_DEFAULT;
		$this->upnptimeout=TIMEOUT_DEFAULT_UPNP;
		$this->upnptimeoutinspect=TIMEOUT_DEFAULT_INSPECT_UPNP;
		$this->upnpiface=IFACE_DEFAULT_UPNP;
		//$this->wsdscript=dirname(__FILE__).'/ponvif-wsd-ext.py';
		$this->wsdscript=getcwd().'/ponvif-wsd-ext.py';
		$this->upnpdscript=getcwd().'/ponvif-upnp-ext.py';
		$this->re_scopes["scopes"]=array('type'=>SCOPES_TYPE_REG,'name'=>SCOPES_NAME_REG,'location'=>SCOPES_LOCATION_REG,'hardware'=>SCOPES_HARDWARE_REG);
		$this->re_types["types"]=array('network'=>TYPES_NETWORK_REG);
		$tags=array('friendlyName','manufacturer','modelDescription','modelName','modelNumber','presentationURL');
		foreach ($tags as $tag) $this->re_device_upnp[$tag]=str_replace('%%TAG%%',$tag,DEVICE_TAG_UPNP_REG);
	}

        public function __destruct()
        {
                // nothing to do
        }

	protected function pythonScript() {
		return $this->wsdscript.' --timeout '.$this->timeout;
	}

	protected function pythonScriptUPNP() {
		return $this->upnpdscript.' server '.$this->upnpiface.' '.$this->upnptimeout;
	}

	protected function wsdiscovery_1($data) {

		$cameras=array();
		$icount=0;

		foreach ($data as $camera) {
        		foreach ($this->re_scopes as $key=>$value) {
                		if (array_key_exists($key,$camera)) {
                        		$elements=$camera[$key];
                        		foreach ($value as $key2=>$val2) {
                                		preg_match_all($val2, $elements, $matches);
                                		if  (count($matches[1])>2)
							$cameras[$icount][ucwords($key)][ucwords($key2)]=$matches[1];
						else
							$cameras[$icount][ucwords($key)][ucwords($key2)]=$matches[1][0];
                        		}
                		}
        		}
        		foreach ($this->re_types as $key=>$value) {
                		if (array_key_exists($key,$camera)) {
                        		$elements=$camera[$key];
                        		foreach ($value as $key2=>$val2) {
                                		preg_match_all($val2, $elements, $matches);
                               			if (count($matches[1])>2)
							$cameras[$icount][ucwords($key)][ucwords($key2)]=$matches[1];
                               			else
							$cameras[$icount][ucwords($key)][ucwords($key2)]=$matches[1][0];
                        		}
                		}
        		}

        		$cameras[$icount]['XAddr']=$camera['xaddr'];

        		$cameras[$icount]['Address']=$camera['epr'];

			foreach ($camera['xaddr'] as $xaddr)
				$cameras[$icount]['IP'][]=parse_url($xaddr, PHP_URL_HOST);

			$icount++;
		}

		return $cameras;
	}

	public function wsdiscovery() {
		if (!is_executable($this->wsdscript)) {
			throw new Exception($this->wsdscript." doesn't exist or is not executable");
		}
		$command = escapeshellcmd($this->pythonScript());
		$output = shell_exec($command);
		return $this->wsdiscovery_1(json_decode($output,true));
	}

	public function upnpdiscovery($checkIfOnvif=false,$filters=array()) {
		if (!is_executable($this->upnpdscript)) {
                        throw new Exception($this->upnddscript." doesn't exist or is not executable");
                }
                $command = escapeshellcmd($this->pythonScriptUPNP());
                $output = shell_exec($command);
                return $this->upnpdiscovery_1(json_decode($output,true),$checkIfOnvif,$filters);
	}

	public function upnpdiscovery_1($data,$checkIfOnvif,$filters) {
                $cameras=array();
                $icount=0;

                foreach ($data as $camera) {
			$passed=true;
			$details=$this->extractUPNPdetails($camera['location']);
			if (!empty($filters)) {
				$passed=false;
				foreach($filters as $key=>$value) {
					if (isset($details[$key]) && stripos($details[$key],$value)!==false) {
						$passed=true;
						break;
					}
				}
			}
			if ($passed) {
				$cameras[$icount]['IP']=$camera['ip'];
				$cameras[$icount]['Details']=$this->extractUPNPdetails($camera['location']);
				$cameras[$icount]['Location']=$camera['location'];
				$cameras[$icount]['USN']=$camera['usn'];
				if ($checkIfOnvif) $cameras[$icount]['ONVIF']=$this->checkIfOnvif($camera['ip']);
				$icount++;
			}
		}

		return $cameras;
	}

	protected function checkIfOnvif($ip) {
		$status='NOTSUPPORTED';
		$url=str_replace('%%IP%%',$ip,CHECKONVIF_UPNP_URL);
		$ch=curl_init();
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_HEADER,true);
		//curl_setopt($ch, CURLOPT_NOBODY,true);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
		curl_setopt($ch, CURLOPT_TIMEOUT, $this->upnptimeoutinspect);
		$output=curl_exec($ch);
		if ( $output  === false) {
			$status='NOTSUPPORTED ('.curl_error($ch).')';
		} else {
			$httpcode=curl_getinfo($ch, CURLINFO_HTTP_CODE);
			if ($httpcode == 200 || $httpcode == 503 || $httpcode == 405) $status=$url;
			else if ($httpcode == 0 && strtolower(trim($output)) === 'service unavailable') $status=$url;
			else if ($httpcode == 404) $status="NOTSUPPORTED";
			//else if ($httpcode == 405) $status="SUPPORTED (enabled?)";
			else $status="NOTSUPPORTED ($httpcode)";
		}
		
		curl_close($ch);
		return $status;
	}

	protected function extractUPNPdetails($xmlfile) {
		$details=array();
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $xmlfile);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_TIMEOUT, $this->upnptimeoutinspect);
		$output = curl_exec($ch);
		$errno = curl_errno($ch);
		if ($errno == 0) {
			foreach ($this->re_device_upnp as $key=>$value) {
				if (preg_match_all($value,$output,$matches)) {
					$details[ucwords($key)]=$matches[1][0];
				}
			}
		}
		return $details;
	}
}
