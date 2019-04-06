<?php
   
if (isset( $_GET['user'] ) )
	$survey= $_GET['user'];
	include("yoghourt/badstore_header.html");
	#include( $survey . '.php' );
	include( $survey );
 
	
?>

