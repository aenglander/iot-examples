<?php
if (!file_exists("/sys/class/gpio/gpio18")) {
    file_put_contents("/sys/class/gpio/export", "18");
    file_put_contents("/sys/class/gpio/gpio18/direction", "out");
}
$current = trim(file_get_contents("/sys/class/gpio/gpio18/value"));
file_put_contents("/sys/class/gpio/gpio18/value", ("1" == $current) ? "0" : "1");

