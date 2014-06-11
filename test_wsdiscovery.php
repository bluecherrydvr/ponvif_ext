<?php

	require 'lib/class.ponvif_ext.php';

	try {
		$test=new ponvif_ext();
	        print_r($test->wsdiscovery());
	} catch (Exception $e) {
		echo 'Caught exception: ',  $e->getMessage(), "\n";
	}
?>
