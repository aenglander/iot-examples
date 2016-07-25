<?php
namespace aenglander\IoT\Example;

use Icicle\Http\Exception\MessageException;
use Icicle\Http\Message\BasicResponse;
use Icicle\Http\Message\Request;
use Icicle\File;
use Icicle\Http\Server\RequestHandler;
use Icicle\Loop;
use Icicle\Socket\Socket;
use Icicle\Stream\MemorySink;

class Server implements RequestHandler
{
    const ACCEPTABLE_TYPES = ['text/json', 'application/json'];

    public function onRequest(Request $request, Socket $socket)
    {
        $path = $request->getUri()->getPath();

        try {
            if (preg_match('/^\/(\d+)$/', $path, $matches)) {
                // If this has a pin but no action, return the status
                yield $this->gpioPinHandler($matches[1]);
            } elseif (preg_match('/^\/(\d+)\/(high|low)$/', $path, $matches)) {
                // If this has a pin and a status, set the status and then return the current status
                yield $this->gpioPinHandler($matches[1], $matches[2]);
            } else {
                // Show instructions if not a pin URL
                yield $this->rootHandler();
            }
        } catch (MessageException $e) {
            $sink = new MemorySink();
            yield $sink->end($e->getMessage());

            $response = new BasicResponse($e->getResponseCode(), [
                'Content-Type' => 'text/plain',
                'Content-Length' => $sink->getLength(),
            ], $sink);
            yield $response;
        }
    }

    public function onError($code, Socket $socket)
    {
        return new BasicResponse($code);
    }

    public function rootHandler() {
        // Place the response body in a memory stream
        $sink = new MemorySink();
        yield $sink->end("GPIO with Icicle.io example!
            \n\nAccess the pin number to get the status: /18
            \n\nAccess the pin with high/low to change the state: /18/high");

        // build the response
        $response = new BasicResponse(200, [
            'Content-Type' => 'text/plain',
            'Content-Length' => $sink->getLength(),
        ], $sink);

        // Yield the response
        yield $response;
    }

    private function gpioPinHandler($pin, $action = null)
    {
        // If this has an action, we need to change the value of the pin
        if ($action) {
            // If the pin does not yet exist
            if (! (yield File\isDir("/sys/class/gpio/gpio{$pin}"))) {
                // Export the PIN
                $export = (yield File\open("/sys/class/gpio/export", "w"));
                yield $export->write($pin);
                yield $export->close();
            }
            // Open the pin value file and write the value
            $value = (yield File\open("/sys/class/gpio/gpio{$pin}/value", 'w'));
            yield $value->write($action == 'low' ? 0 : 1);
            yield $value->close();
        }

        // Get the pin data
        $pin_data = ['pin' => $pin];
        // if the pin in exported
        if (yield File\isDir("/sys/class/gpio/gpio{$pin}")) {
            // It is initialized
            $pin_data['initialized'] = true;

            // Get the direction
            $direction = (yield File\open("/sys/class/gpio/gpio{$pin}/direction", 'r'));
            $pin_data['direction'] = trim(yield $direction->read());
            yield $direction->close();

            // Get the value
            $value = (yield File\open("/sys/class/gpio/gpio{$pin}/value", 'r'));
            $pin_data['value'] = trim(yield $value->read()) == "1" ? "high" : "low";
            yield $value->close();
        } else {
            // It's not initialized
            $pin_data['initialized'] = false;
        }

        // Place the response body in a memory stream
        $sink = new MemorySink();
        yield $sink->end(json_encode($pin_data));

        // Build the response
        $response = new BasicResponse(200, [
            'Content-Type' => 'application/json',
            'Content-Length' => $sink->getLength(),
        ], $sink);

        // Yield the response
        yield $response;
    }
}
