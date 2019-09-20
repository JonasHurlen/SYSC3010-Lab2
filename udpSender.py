"""
modified from original source: https://pymotw.com/2/socket/udp.html
this program is designed to send UDP messages and then wait for an acknoledgement
"""

# Source: https://pymotw.com/2/socket/udp.html

# max size of data that will be parsed as a single message.
MAXDATASIZE = 2**8

import socket, sys, time

import argparse

def make_arg_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("addr", type=str,
                        help="specifies the IP send data to")
    parser.add_argument("port", type=int,
                        help="port to listen on")
    parser.add_argument("nReps", type=int, default=1,
                        help="number of repeated messages to send, each message is suffixed by an index.")
    parser.add_argument("--usePrompt", action="store_true",
                        help="by default this will just send 'Message#' nReps times, with this flag instead the user is prompted to enter messages")
    return parser
def parse_command_line_arguments(args=None):
    args = make_arg_parser().parse_args(args)
    if(args.usePrompt):
        args.messageIter = iter(getInput, b'')
    else:
        args.messageIter = (b'Message'+str(idx).encode() for idx in range(args.nReps))
    args.target = (args.addr, args.port)
    print(args)
    return args


def getSocket(target):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(target)
    return s
def getInput():
    return input("data to send (enter to exit):").encode()

def main(list_of_args=None):
    args = parse_command_line_arguments(list_of_args)
    with getSocket(args.target) as s:
        for message in args.messageIter:
            sendallto(s, message, (args.addr, args.port))
            print("sent", message)
            buf, source = s.recvfrom(MAXDATASIZE)
            if not len(buf):
                return
            print("Received acknoledge from {}: {}".format(source, buf))
            if(source != args.target):
                cont = input("got message from non original target, enter anything to exit or just hit enter to continue")
                if cont: #anything was entered
                    return

def sendallto(sock, data, target):
    while data:
        bsent = sock.sendto(data, target)
        data = data[bsent:]


if __name__ == "__main__":
    main() # ["127.0.0.1","9999", "5"])
