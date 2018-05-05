import pings
import smtplib
import time
import socket
import logging
import argparse

# {{{ Logging

logging.basicConfig()
log = logging.getLogger("check_forever")
log.setLevel('INFO')

#

# {{{ Args

LISTENING_PORT    = 4569
SMTP_SERVER       = "smtp.gmail.com"
SMTP_PORT         = 587
SENDER_EMAIL      = ""
SENDER_EMAIL_PASS = ""
DESTINATION_EMAIL = ""

parser = argparse.ArgumentParser(description='Check if a ping server is alive, forever. If not, an email is sent')
parser.add_argument("--listening_port",
                    help="Listening port"
                    default=LISTENING_PORT)
parser.add_argument("--smtp_server",
                    help="SMTP server"
                    default=SMTP_SERVER)
parser.add_argument("--smtp_port",
                    help="SMTP port"
                    default=SMTP_PORT)
parser.add_argument("--sender_email",
                    help="Sender email"
                    default=SENDER_EMAIL)
parser.add_argument("--sender_email_pass",
                    help="Sender email password"
                    default=SENDER_EMAIL_PASS)
parser.add_argument("--destination_email",
                    help="Destination email of the messages"
                    default=SENDER_EMAIL_PASS)

args = parser.parse_known_args()[0]
listening_port    = int(args.listening_port)
smtp_server       = args.smtp_server
smtp_port         = int(args.smtp_port)
sender_email      = args.sender_email
sender_email_pass = args.sender_email_pass
destination_email = args.destination_email

# }}}

# {{{ Listen to LISTENING_PORT to get the source address

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', LISTENING_PORT))
sock.listen(1)
print("Listening at: " +  str(LISTENING_PORT))
conn, addr = sock.accept()

host = addr[0]
print("Host = " + host)

# }}}

# {{{ Log-in into the SMTP server

# http://naelshiab.com/tutorial-send-email-python/
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(sender_email, sender_email_pass)

# }}}

# {{{ Ping the host, forever

p = pings.Ping()

while True:
    
    # https://github.com/satoshi03/pings
    response = p.ping(host)
    while response.is_reached():
        print(":-)")
        response = p.ping(host)

    print(":-(")

    msg = "host " + host + "dead"
    server.sendmail(sender_email, destination_email, msg)
    server.quit()

    time.sleep(1)

# }}} 
