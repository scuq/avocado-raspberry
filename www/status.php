<?php

function getStatus() {
	$status="unkown";	
	if (file_exists('/var/lib/avocado/status.txt')) {
		$fh = fopen('/var/lib/avocado/status.txt','r') or die($php_errormsg);

		$status = fread($fh,filesize('/var/lib/avocado/status.txt'));
	}
	echo $status;
	return;
}
	

?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="refresh" content="3" />
<title>Avocado</title>
<style type="text/css" media="screen">
body { background: #e7e7e7; font-family: Verdana, sans-serif; font-size: 11pt; }
#page { background: #ffffff; margin: 50px; border: 2px solid #c0c0c0; padding: 10px; }
#header { background: #5b793a; border: 2px solid #7590ae; text-align: center; padding: 10px; color: #ffffff; }
#header h1 { color: #ffffff; }
#body { padding: 10px; }
span.tt { font-family: monospace; }
span.bold { font-weight: bold; }
a:link { text-decoration: none; font-weight: bold; color: #5b793a; background: #fff; }
a:visited { text-decoration: none; font-weight: bold; color: #5b793a; background: #fff; }
a:active { text-decoration: none; font-weight: bold; color: #5b793a; background: #fff; }
a:hover { text-decoration: none; color: #5b793a; background: #aaa; }
</style>
<script type="text/JavaScript">
<!--
function timedRefresh(timeoutPeriod) {
	setTimeout("location.reload(true);",timeoutPeriod);
}
//   -->
</script>
</head>
<body onload="JavaScript:timedRefresh(3000);>
<div id="page">
 <div id="header">
 <h1><img src="images/avocado.png" alt="Avocado"></h1>
 </div>
 <div id="body">
<h2><?php getStatus(); ?></h2>
</div>
 <div id="header">
<h1><?php echo date("Y-m-d H:i:s"); ?></h1>
 </div>
  </body>
</html>

