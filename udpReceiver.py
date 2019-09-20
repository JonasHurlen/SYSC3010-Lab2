"""
modified from original source: https://pymotw.com/2/socket/udp.html
this program is designed to recieve UDP messages and send back an acknoledgement
in the form of "ACK:" followed by original message.
"""

# Source: https://pymotw.com/2/socket/udp.html

# max size of data that will be parsed as a single message.
MAXDATASIZE = 2**8

import socket, sys, time

import argparse

def make_arg_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("port", type=int, help="port to listen on")
    parser.add_argument("--ownHost", type=str, default="0.0.0.0",
                        help="""
specifies the IP to bind the reciever on,
defaults to 0.0.0.0 so allow all connections
can specify the IP of *this machine* to accept differently""")
    return parser


def getSocket(addr, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((addr, port))
    return s

def main(list_of_args=None):
    args = make_arg_parser().parse_args(list_of_args)
    print(args)
    with getSocket(args.ownHost, args.port) as s:
        while True:

            print ("Waiting to receive on port {0.port} : press Ctrl-C or Ctrl-Break to stop ".format(args))

            buf, address = s.recvfrom(MAXDATASIZE)
            if not len(buf):
                break
            print ("Received %s bytes from %s %s: " % (len(buf), address, buf ))
            sendallto(s, b"ACK:"+buf, address)

def sendallto(sock, data, addr):
    while data:
        bsent = sock.sendto(data, addr)
        data = data[bsent:]


if __name__ == "__main__":
    main(["9999"])
