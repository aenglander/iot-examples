IoT Examples for Python Twisted
===============================

This project contains an example for running a true IoT server with Python and 
[Twisted](https://twistedmatrix.com/trac/) for async I/O.

Requirements
------------

### Raspberry Pi

* python-dev
* libffi-dev
* libssl-dev

To install the requirements via Aptitude in Raspbian, run the following command at a terminal:

```bash
sudo apt-get install -y python-dev libffi-dev libssl-dev
```

Installation
------------

Use Easy Install to setup the server:

```bash
python setup.py develop
```

Run the Server
--------------

Depending on the platform, run the appropriate file:

### Raspberry Pi

```bash

python pi-server.py

```

### Intel Edison

```bash

python edison-server.py

```
