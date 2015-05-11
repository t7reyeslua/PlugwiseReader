<?php
require_once 'connect.php';

if (!$con)
{
die("Connection failed: " . mysqli_connect_error());
}

$smile_id = $_POST['name'];
$measurement_timestamp = $_POST['timestamp'];
$current_power = $_POST['power'];
$directionality = $_POST['directionality'];
$unit = $_POST['unit'];
$tariff_indicator = $_POST['tariff_indicator'];
$interv = $_POST['interval'];
$service = $_POST['service_type'];

$sql = "INSERT INTO smile (smile_id, measurement_timestamp, power, directionality, unit, tariff_indicator, interv, service_type) VALUES ('$smile_id', '$measurement_timestamp', '$current_power', '$directionality', '$unit', '$tariff_indicator', '$interv', '$service');";

if (!mysqli_query($con,$sql))
{
die("Problem with query: " .  mysqli_error($con));
}

?>
