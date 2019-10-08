<?php

function SqlQuery($query)
{
	$host	= "localhost";
	$user	= "scriptl1_tgbot";
	$pwd	= "790th790th";
	$dbase	= "scriptl1_wp_e3c7";
	$answerLine	= "";

	$link = mysqli_connect($host, $user, $pwd, $dbase);

	/* check connection */
	if (mysqli_connect_errno()) {
	    $answerLine	= $answerLine."Unable to connect DB: %s\n".mysqli_connect_error();
	    exit();
	}

	/* run multiquery */
	if (mysqli_multi_query($link, $query)) {
	    //do {
	        /* get first result data */
	        if ($result = mysqli_store_result($link)) {
	            while ($row = mysqli_fetch_row($result)) {
	                $answerLine	= $answerLine.implode(' # ',$row)."\n";
	            }
	            mysqli_free_result($result);
	        }
	        /* print divider */
	        if (mysqli_more_results($link)) {
	        	$answerLine	= $answerLine."### ";
	        }

	    //} while (mysqli_next_result($link));
	}
	/* close connection */
	mysqli_close($link);

	return $answerLine;

}
//if (file_exists('error_log')) unlink('error_log');
$moken=preg_replace('/\s+/', '', SqlQuery('SELECT matrix.mind FROM `matrix` as matrix where matrix.person="fpv_rover_bot"'));
$botUrl = "https://api.telegram.org/bot".$moken."/sendPhoto?chat_id=".$_GET['user'];
$ch = curl_init();
curl_setopt($ch, CURLOPT_HTTPHEADER, array("Content-Type:multipart/form-data"));
curl_setopt($ch, CURLOPT_URL, $botUrl);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, array("photo" => "@".$_GET['photoUrl'],));
$output = curl_exec($ch);
print $output;
?>