Curio
=====

**This is extremely experimental and uses functionality in Curio that is not yet released.
You must manually install the Curio library from source from 
[this commit](https://github.com/dabeaz/curio/commit/7d459a6bbba73b616e56f388eb095f2c58492d84) or later.**

Requires Python 3.5+

Server controlled via telnet at port 25000. Takes data in the form of {pin}{value}, i.e. `401`
would send a command to turn pin 40 on. The server returns `OK` on success and `ERROR` on 
failure.

