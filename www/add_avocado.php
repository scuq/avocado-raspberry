<?php

	$avocado_item="";
	$avocado_type="";
	$avocado_timeout="30m";
	$return_code=99;
	$statusmsg="";

	if (isset($_POST["submit_add"])) {

		if ( isset($_POST["txt_avocado_item"]) and isset($_POST["radio_type"]) ) {

			$avocado_item=$_POST["txt_avocado_item"];
			$avocado_type=$_POST["radio_type"];

			if (isset($_POST["text_timeout"])) {
				if ($_POST["text_timeout"] != "") {
					$avocado_timeout=$_POST["text_timeout"];
				}
			}



			ob_start();
			passthru ("/usr/local/bin/avocado -t ".$avocado_type." -a ".$avocado_item." -o ".$avocado_timeout."  2>&1",$return_code);
			$results = ob_get_contents();
			ob_end_clean();

			if ($return_code == 0) {
				$statusmsg="Avocado Item added to queue.";

			} else {
				$statusmsg="Failed to add item to avocado queue!";
				$statusmsg=$statusmsg."<BR>".$results;
			}
			

		}

	}


?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Add Avocado</title>
<style type="text/css" media="screen">
body { background: #e7e7e7; font-family: Verdana, sans-serif; font-size: 11pt; }
#page { background: #ffffff; margin: 50px; border: 2px solid #c0c0c0; padding: 10px; }
#header { background: #5b793a; border: 2px solid #7590ae; text-align: center; padding: 10px; color: #ffffff; }
#back { background: #5b793a; border: 0px solid #7590ae; text-align: left; padding: 10px; color: #ffffff; }
#header h1 { color: #ffffff; }
#body { padding: 10px; }
span.tt { font-family: monospace; }
span.bold { font-weight: bold; }
a:link { text-decoration: none; font-weight: bold; color: #5b793a; background: #fff; }
a:visited { text-decoration: none; font-weight: bold; color: #5b793a; background: #fff; }
a:active { text-decoration: none; font-weight: bold; color: #5b793a; background: #fff; }
a:hover { text-decoration: none; color: #5b793a; background: #aaa; }
.wmfg_layout_1, table, .wmfg_textarea { font-family: Verdana, Geneva, sans-serif; font-size: 13px; }
.wmfg_layout_1 ul.wmfg_questions { list-style-type: none; margin: 0; padding: 0; }
.wmfg_layout_1 ul.wmfg_questions li.wmfg_q { margin: 10px 0; }
.wmfg_layout_1 label.wmfg_label { display: block; margin: 0 0 5px 0; font-weight:bold; }
.wmfg_layout_1 table.wmfg_answers { width: 100%; _width: 97%; border-collapse: collapse; }
.wmfg_layout_1 table.wmfg_answers { vertical-align: top; }
.wmfg_layout_1 table.wmfg_answers td { padding: 2px; vertical-align: top; }
.wmfg_layout_1 table.wmfg_answers td.wmfg_a_td { width: 25px; }

.wmfg_layout_1 .wmfg_text { border: 1px solid #CCC; padding: 4px; font-size: 13px; color: #000000; width: 98.5%;
background-color: #ffffff;
background:-webkit-gradient(linear,0 0,0 100%,from(#f8f8f8),to(#fff));
background:-moz-linear-gradient(top,#f8f8f8,#fff);
}
.wmfg_layout_1 .wmfg_textarea { border: 1px solid #CCC; padding: 4px; font-size: 13px; color: #000000; width: 98.5%;
background:-webkit-gradient(linear,0 0,0 100%,from(#f8f8f8),to(#fff));
background:-moz-linear-gradient(top,#f8f8f8,#fff);
background-color: #ffffff;
}
.wmfg_layout_1 .wmfg_select { 
border:1px solid #CCCCCC; padding: 3px; font-size: 13px; color: #000000; margin: 0; width: 100%; _width: 97%;
background-color: #ffffff;
background:-webkit-gradient(linear,0 0,0 100%,from(#f8f8f8),to(#fff));
background:-moz-linear-gradient(top,#f8f8f8,#fff);
}
.wmfg_layout_1 .wmfg_btn { 
border: 1px solid #cccccc; cursor: pointer; font-weight: normal; font-size: 13px; padding: 6px; color: #444; font-family: 'lucida grande', tahoma, verdana, arial, sans-serif; 
background: -webkit-gradient(linear, left top, left bottom, from(#FAFAFA), color-stop(0.5, #FAFAFA), color-stop(0.5, #E5E5E5), to(#F9F9F9)); 
background: -moz-linear-gradient(top, #FAFAFA, #FAFAFA 50%, #E5E5E5 50%, #F9F9F9);
filter: progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#FAFAFA', endColorstr='#E5E5E5');
}
.wmfg_layout_1 .wmfg_btn:hover {  
background: -webkit-gradient(linear, left top, left bottom, from(#EDEDED), color-stop(0.5, #EDEDED), color-stop(0.5, #D9D9D9), to(#EDEDED)); 
background: -moz-linear-gradient(top, #EDEDED, #EDEDED 50%, #D9D9D9 50%, #EDEDED);
filter: progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#E3326E', endColorstr='#D9D9D9'); 
</style>
</head>
<body>
 <div id="back">
 <a href="/">&lt;&lt;&lt;back</a>
 </div>
 <div id="header">
 <h1>Add Avocado to Queue</h1>
 </div>
<div style="width:600px" class="wmfg_layout_1">

<form method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>">

<ul class="wmfg_questions">

	<li class="wmfg_q">
		<label class="wmfg_label" for="textarea_id">Avocado Item</label>
		<textarea class="wmfg_textarea" name="txt_avocado_item" id="txt_avocado_item" style="height:80px"></textarea>
	</li>

	<li class="wmfg_q">
		<label class="wmfg_label">Avocado Type</label>
		<table class="wmfg_answers">
			<tr class="wmfg_a">
				<td class="wmfg_a_td"><input type="radio" class="wmfg_radio" name="radio_type" value="youtube" /></td>
				<td><label class="wmfg_label_a" for="radio_1">Youtube</label></td>
			</tr>
			<tr class="wmfg_a">
				<td class="wmfg_a_td"><input type="radio" class="wmfg_radio" name="radio_type" value="pics" /></td>
				<td><label class="wmfg_label_a" for="radio_2">Picture (Local Picture Show)</label></td>
			</tr>
			<tr class="wmfg_a">
				<td class="wmfg_a_td"><input type="radio" class="wmfg_radio" name="radio_type" value="webbrowse" /></td>
				<td><label class="wmfg_label_a" for="radio_3">Web (Browse to this URL)</label></td>
			</tr>
			<tr class="wmfg_a">
				<td class="wmfg_a_td"><input type="radio" class="wmfg_radio" name="radio_type" value="stream" /></td>
				<td><label class="wmfg_label_a" for="radio_3">Stream (Video Streaming URL)</label></td>
			</tr>
			<tr class="wmfg_a">
				<td class="wmfg_a_td"><input type="radio" class="wmfg_radio" name="radio_type" value="test" /></td>
				<td><label class="wmfg_label_a" for="radio_3">Test</label></td>
			</tr>
		</table>
	</li>

	<li class="wmfg_q">
		<label class="wmfg_label" for="text_id">Timeout (default 30m)</label>
		<input type="text" class="wmfg_text" name="text_timeout" id="text_timeout" value="" />
	</li>

	<li class="wmfg_q">
		<input type="submit" class="wmfg_btn" name="submit_add" id="submit_add" value="Add" />
	</li>

</ul>

</form>

</div>
 <div id="header">
<h1><?php echo $statusmsg; ?></h1>
 </div>
 <div id="header">
<h1><?php echo date("Y-m-d H:i:s"); ?></h1>
 </div>
 </body>
</html>
