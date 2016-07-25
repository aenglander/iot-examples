#!/usr/bin/env php
<?php

require __DIR__ . '/vendor/autoload.php';

use aenglander\IoT\Example\Server;
use Icicle\Http\Server\Server as HttpServer;
use Icicle\Loop;

$server = new HttpServer(new Server());

$server->listen(8080, '0.0.0.0');

Loop\run();

