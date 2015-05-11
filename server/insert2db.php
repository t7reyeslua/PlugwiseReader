<?php
require_once 'connect.php';

if (!$con)
{
die("Connection failed: " . mysqli_connect_error());
}

$plug_id = $_POST['name'];
$measurement_timestamp = $_POST['timestamp'];
$current_power = $_POST['power'];

$sql = "INSERT INTO log (plug_id, measurement_timestamp, current_power) VALUES ('$plug_id', '$measurement_timestamp', '$current_power');";

if (!mysqli_query($con,$sql))
{
die("Problem with query: " .  mysqli_error($con));
}

?>