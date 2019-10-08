<?php
//$group='106129214';

/* PUT данные приходят в потоке ввода stdin */
$putdata = fopen("php://input", "r");

/* Открываем файл на запись */
$filename="".uniqid().".jpg";
$fp = fopen($filename, "w");

/* Читаем 3 MB данных за один раз
   и пишем в файл */
while ($data = fread($putdata, 3000000)) fwrite($fp, $data);
fclose($fp);
fclose($putdata);

//$log = fopen("log.txt", "w");
$handle = fopen($filename, "rb");
$contents = fread($handle, filesize($filename));
$group='';
$clear_contents='';
$group_read_complete=false;
for ($i=0;$i<filesize($filename);$i++)
{
	if ($group_read_complete) $clear_contents.=$contents[$i];
	else
	{
		if ($contents[$i]=='#') $group_read_complete=true;
		else $group.=$contents[$i];
	}	
}

//fwrite($log,$group);
//fclose($log);

$clear_filename="".uniqid().".jpg";
$clear_fp = fopen($clear_filename, "w");
fwrite($clear_fp,$clear_contents);
fclose($clear_fp);

//send to telegram and remove file
file_get_contents("http://scriptlab.net/telegram/bots/fpv_rover_bot/relayPhoto.php?user=$group&photoUrl=scriptlab.net/telegram/bots/fpv_rover_bot/$clear_filename");
unlink($filename);
unlink($clear_filename);
?>