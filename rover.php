<?php
//cd /etc/apache2/
//sudo nano apache2.conf
//User pi
//Group pi

//sudo visudo
//www-data ALL=(ALL) NOPASSWD: ALL
//http://192.168.1.30/rover.php?cmd=10,10,1000:-10,-10,1000:10,-10,1000

$command = 'python3 rover.py '.$_GET['cmd'].' 2>&1';
$pid = popen( $command,"r");
while( !feof( $pid ) )
{
	 echo fread($pid, 256);
	 flush();
	 ob_flush();
	 usleep(100000);
}
pclose($pid);
?>
