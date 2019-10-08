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

if ($text=='/f@fpv_rover_bot' || $text=='/f') $text='m,1,1,1';
if ($text=='/b@fpv_rover_bot' || $text=='/b') $text='m,-1,-1,1';
if ($text=='/l@fpv_rover_bot' || $text=='/l') $text='m,-1,1,0.4';
if ($text=='/r@fpv_rover_bot' || $text=='/r') $text='m,1,-1,0.4';
if ($text=='/p@fpv_rover_bot' || $text=='/p') $text='p,1280,1280,200';
if ($text=='/n@fpv_rover_bot' || $text=='/n') $text='n,1280,1280,200';

$cmd=substr($text,0,2);
if ($cmd=='m,'||$cmd=='p,'||$cmd=='n,')
{

	if ($user=='106129214'||$chat=='-384403215')//me,fpv,lhome ||$chat=='-23709374', lunch ||$chat=='-161324915'
	{
		//$AnswerText='disabled due charging';
		$AnswerText=file_get_contents('http://95.165.139.53/rover.php?cmd='.str_replace("\n",",$chat:",$text).",$chat");
	}
	else $AnswerText='You are not authorized to use this bot';

	if ($AnswerText!='') sendMessage($chat,$AnswerText);
	
}
?>