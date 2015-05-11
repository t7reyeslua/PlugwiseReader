<?php

//Change to corresponding values
$servername = "localhost";
$username = "USERNAME";
$password = "PASSWORD";
$dbname = "DBNAME";

$con = mysqli_connect($servername, $username, $password, $dbname);

if (!$con)
{
die("Connection failed: " . mysqli_connect_error());
}

?>
