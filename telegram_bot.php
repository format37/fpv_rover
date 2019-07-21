<?php
function SqlQuery($query)
{
	$host	= "localhost";
	$user	= "usr";
	$pwd	= "pwd";
	$dbase	= "dbase";
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

function sendMessage($chatID, $messaggio) {
	$moken=preg_replace('/\s+/', '', SqlQuery('SELECT matrix.mind FROM `matrix` as matrix where matrix.person="fpv_rover_bot"'));
    $url = "https://api.telegram.org/bot" . $moken . "/sendMessage?chat_id=" . $chatID;
    $url = $url . "&text=" . urlencode($messaggio);
    $ch = curl_init();
    $optArray = array(
            CURLOPT_URL => $url,
            CURLOPT_RETURNTRANSFER => true
    );
    curl_setopt_array($ch, $optArray);
    $result = curl_exec($ch);
    curl_close($ch);
    return $result;
}

$json = file_get_contents('php://input');
$action = json_decode($json, true);
$text	= $action['message']['text'];
$chat		= $action['message']['chat']['id'];
$user		= $action['message']['from']['id'];
$text = strtolower($text);
$AnswerText	= '';

if ($user=='106129214')
{
	//if (substr($text,0,6)=='/help ') $AnswerText	= file_get_contents('http://95.165.139.53/rover.php?cmd='.substr($text,5));
	//if (substr($text,0,5)=='/cmd ') $AnswerText	= file_get_contents('http://95.165.139.53/rover.php?cmd='.substr($text,5));
	//$AnswerText=substr($text,5);
	file_get_contents('http://YOUR_BOT_IP/rover.php?cmd='.str_replace("\n",":",$text));
}
else $AnswerText='You are not authorized to use this bot';

if ($AnswerText!='') sendMessage($chat,$AnswerText);
?>