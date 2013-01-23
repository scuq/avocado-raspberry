<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Avocado Cache</title>
<style type="text/css" media="screen">
body { background: #e7e7e7; font-family: Verdana, sans-serif; font-size: 11pt; }
#page { background: #ffffff; margin: 50px; border: 2px solid #c0c0c0; padding: 10px; }
#header { background: #5b793a; border: 2px solid #7590ae; text-align: center; padding: 10px; color: #ffffff; }
#back { background: #5b793a; border: 0px solid #7590ae; text-align: left; padding: 10px; color: #ffffff; }
#header h1 { color: #ffffff; }
#body { padding: 10px; }
span.tt { font-family: monospace; }
span.bold { font-weight: bold; }
td { padding:20px; }
a:link { text-decoration: none; font-weight: bold; color: #5b793a; background: #fff; }
a:visited { text-decoration: none; font-weight: bold; color: #5b793a; background: #fff; }
a:active { text-decoration: none; font-weight: bold; color: #5b793a; background: #fff; }
a:hover { text-decoration: none; color: #5b793a; background: #aaa; }
</style>
</head>
<body>
 <div id="back">
 <a href="/">&lt;&lt;&lt;back</a>
 </div>
 <div id="header">
 <h1>Cached Avocados</h1>
 </div>

<?php
    ob_start();
    passthru ("/usr/local/bin/avocado -c --html 2>&1");
    $results = ob_get_contents();
    ob_end_clean();
    echo $results;
//echo "<pre>$output</pre>";
?>
 <h1><a href="flushc.php">flush</a></h1>
 </body>
</html>
