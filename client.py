# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from multiprocessing import *
import threading
import struct
import getch
from socket import *
import time
import select

TEAMNAME = 'IN'
TXT_ENCODING = 'utf-8'
NUM_ENCODING = "little"
CLIENT_STARTED_MSG = 'Client started, listening for offer requests...'
RCVD_OFFER_MSG = 'Received offer from {} : {},\nattempting to connect...'
IMPOSTER_OFFER_MSG = 'An imposter server ({})tried to connect, but it had failed.'
FAILED_TO_CONNECT_MSG = 'Failed to connect'
MAGIC_COOKIE = b'\xba\xdc\xcd\xab'
MSG_TYPE_OFFER = 0x02
BUFFER_SIZE = 1024
UDP_PORT = 13117


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def looking_for_server_state():
    print(bcolors.OKBLUE + CLIENT_STARTED_MSG + bcolors.ENDC)
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind(('', UDP_PORT))
        m = s.recvfrom(BUFFER_SIZE)
        receivedbytes = m[0]
        cookie = receivedbytes[0:4]
        op = receivedbytes[4]
        portbytes = receivedbytes[6:8]
        (port,) = struct.unpack('H',portbytes)
        serverip = m[1][0]
        if (cookie == MAGIC_COOKIE) & (op == MSG_TYPE_OFFER):
            print(bcolors.OKGREEN+RCVD_OFFER_MSG.format(serverip,port)+bcolors.ENDC)
            return serverip, port
        else:
            hexadecimal_string = receivedbytes.hex()
            print(hexadecimal_string)
            print(bcolors.FAIL+IMPOSTER_OFFER_MSG.format(serverip)+bcolors.ENDC)
            return looking_for_server_state()
    except Exception as e:
        print(e)

    return None, None


def connect_to_server_state(serverip, port):
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((serverip, port))
        return s
    except Exception as e:
        print(e)
    return None


def multi_gamemode_senddata(sock,pipe):
    try:
        i, _, _ = select.select( [pipe], [], [])
        while True:
            if(i):
                data = pipe.recv()
                print(bcolors.BOLD+data+bcolors.ENDC)
                sock.send(data.encode(TXT_ENCODING))
    except Exception as e:
        print(e)
    pass


def multi_gamemode_downloaddata(sock):
    try:
        data = sock.recv(BUFFER_SIZE)
        if data != "":
            data = str(data, TXT_ENCODING)
            print(bcolors.OKCYAN+data+bcolors.ENDC)
        data = sock.recv(BUFFER_SIZE)
        if data != "":
            data = str(data, TXT_ENCODING)
            print(bcolors.BOLD+data+bcolors.ENDC)
    except Exception as e:
        print(e)
    pass


def theloop(pipe):
    (serverip, port) = looking_for_server_state()
    tcpsocket = connect_to_server_state(serverip, port)
    if tcpsocket == None:
        print(bcolors.WARNING + FAILED_TO_CONNECT_MSG+bcolors.ENDC)
        theloop(pipe)
    else:
        #first, lets flush away all data from the "getch" pipe
        if pipe.poll():
            pipe.recv()
        #send the name
        tcpsocket.send(bytes(TEAMNAME, TXT_ENCODING))
        downloading = Process(target=multi_gamemode_downloaddata, args=(tcpsocket,))
        uploading = Process(target=multi_gamemode_senddata, args=(tcpsocket,pipe,))
        downloading.start()
        uploading.start()
        downloading.join()
        uploading.kill()
        theloop(pipe)

def getchfun(pipe):
    try:
        while True:
            data = getch.getch()
            pipe.send(data)
    except Exception as e:
        print(e)
    pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    r1, w1 = Pipe(duplex=False)
    getchproc = Process(target=getchfun,args=(w1,))
    getchproc.start()
    theloop(r1)

