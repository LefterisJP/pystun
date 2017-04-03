#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Options:
    --nostun            Use a bare socket without STUN.
    -v                  DEBUG logging.
    -p=<local_port>     Port of local socket [default: 4200].

Usage:
    teststun [-v] [--nostun] receive [-p=<local_port>]
    teststun [-v] [--nostun] send [-p=<local_port>] <target_ip> <target_port> [<msg>...]
"""
import logging
import socket
from contextlib import contextmanager

import stun
from docopt import docopt


log = logging.getLogger(__name__)


@contextmanager
def stun_socket(
    source_ip='0.0.0.0',
    source_port=4200,
    stun_host=None,
    stun_port=3478
):
    with open_bare_socket(source_ip=source_ip, source_port=source_port) as sock:
        print "Initiating STUN"
        nat_type, nat = stun.get_nat_type(
            sock,
            source_ip,
            source_port,
            stun_host=stun_host,
            stun_port=stun_port
        )
        external_ip = nat['ExternalIP'],
        external_port = nat['ExternalPort']
        log.debug(nat)
        print "STUN-socket ready: {3} {4} external: {0} {1} [{2}]".format(
            external_ip[0] or 'unknown',  # for some reason 'Test3' returns 'None' in some cases
            external_port or 'unknown',
            nat_type,
            *sock.getsockname()
        )
        yield sock


@contextmanager
def open_bare_socket(
    source_ip='0.0.0.0',
    source_port=42000
):
    sock = socket.socket(
        socket.AF_INET,  # Internet
        socket.SOCK_DGRAM  # UDP
    )

    sock.settimeout(2)
    sock.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )
    sock.bind(
        (source_ip, source_port)
    )
    print "socket ready: {0} {1} [bare socket]".format(
        *sock.getsockname()
    )
    yield sock
    sock.close()

# `--nostun` changes this to `open_bare_socket`
open_socket = stun_socket


def receive(source_port):
    with open_socket(source_port=source_port) as sock:
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                print "received: {} from {}".format(data, addr)
                if data.lower().startswith("close"):
                    print "CLOSE received"
                    # break
            except socket.timeout:
                pass


def send(target_address, target_port, msgs, source_port=4200):
    target = (target_address, target_port)
    with open_socket(source_port=source_port) as sock:
        sendtrace(sock, 'HELOHELO', target)
        for msg in msgs:
            sendtrace(sock, msg, target)
        sendtrace(sock, 'CLOSE', target)


def sendtrace(sock, msg, target):
    """Send `msg` through `sock` to `target` and trace via print.
    """
    print "sending '{}' to '{} {}'".format(msg, *target)
    sock.sendto(msg, target)


if __name__ == "__main__":
    options = docopt(__doc__)
    if options['-v']:
        logging.basicConfig(level=logging.DEBUG)
        print options
    if options['--nostun']:
        open_socket = open_bare_socket
    if options['send']:
        send(
            options['<target_ip>'],
            int(options['<target_port>']),
            options['<msg>'],
            source_port=int(options['-p']),
        )
    elif options['receive']:
        receive(
            source_port=int(options['-p'])
        )
