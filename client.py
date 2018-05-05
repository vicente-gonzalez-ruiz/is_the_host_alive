#!/usr/bin/env python3

import socket
import logging
import argparse

# {{{ Logging

logging.basicConfig()
log = logging.getLogger("check_forever")
log.setLevel('INFO')

#

# {{{ Args

SERVER = ""
PORT   = 4569

parser = argparse.ArgumentParser(description='Connects with a pinger to show the my IP address')
parser.add_argument("--server",
                    help="Pinger server"
                    default=SERVER)
parser.add_argument("--port",
                    help="Pinger port"
                    default=PORT)

args = parser.parse_known_args()[0]
server = args.server
port   = int(args.port)

# }}}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((server, port))
s.close()
