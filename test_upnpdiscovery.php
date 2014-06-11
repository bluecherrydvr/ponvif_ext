<?php

	require 'lib/class.ponvif_ext.php';

	try {
		$test=new ponvif_ext();
	        print_r($test->upnpdiscovery(true,array('ModelName'=>'camera','ModelDescription'=>'camera')));
	} catch (Exception $e) {
		echo 'Caught exception: ',  $e->getMessage(), "\n";
	}
?>
