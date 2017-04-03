PyStun
======
This is a research fork of https://github.com/jtriley/pystun -- don't bother with
PR's/issues against this repository!

Installation
------------
To install

    $ pip install -r requirements.txt
    $ pip install -e . 

To run the `teststun.py` script:

    Options:
        --nostun            Use a bare socket without STUN.
        -v                  DEBUG logging.
        -p=<local_port>     Port of local socket [default: 4200].

    Usage:
        teststun [-v] [--nostun] receive [-p=<local_port>]
        teststun [-v] [--nostun] send [-p=<local_port>] <target_ip> <target_port> [<msg>...]
    
Example with two hosts:

    # start a listener on host1 on port 4200
    host1 $ ./teststun.py receive

    # try sending to host1 (depending on NAT, this may fail/not be received)
    host2 $ ./teststun.py send host1 4200 hello from host2

    # punch open the port for host1 -> host2 (use second terminal)
    host1 $ ./teststun.py send host2 4200

    # now host2 should be able to get through NAT
    host2 $ ./teststun.py send host1 4200 finally you see me

However, depending on the NAT-type, the same sequence would work the exact same way without STUN -- this is just basic UDP hole punching.

    # start a listener on host1 on port 4200
    host1 $ ./teststun.py --nostun receive

    # try sending to host1 (depending on NAT, this may fail/not be received)
    host2 $ ./teststun.py --nostun send host1 4200 hello from host2

    # punch open the port for host1 -> host2 (use second terminal)
    host1 $ ./teststun.py send --nostun host2 4200

    # now host2 should be able to get through NAT
    host2 $ ./teststun.py send --nostun host1 4200 finally you see me

LICENSE
-------
MIT
