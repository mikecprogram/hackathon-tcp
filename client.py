# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import threading
import getch
from socket import *

TEAMNAME = 'IN'
TXT_ENCODING = 'utf-8'
NUM_ENCODING = "little"
CLIENT_STARTED_MSG = 'Client started, listening for offer requests...'
RCVD_OFFER_MSG = 'Received offer from {},\nattempting to connect...'
IMPOSTER_OFFER_MSG = 'An imposter server ({})tried to connect, but it had failed.'
FAILED_TO_CONNECT_MSG = 'Failed to connect'
MAGIC_COOKIE = b'\xab\xcd\xdc\xba'
MSG_TYPE_OFFER = b'\x02'
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
        serverip = m[1][0]
        if receivedbytes[0:5] == b'\xab\xcd\xdc\xba\x02':
            receivedport = int.from_bytes(receivedbytes[5:7], NUM_ENCODING)
            print(RCVD_OFFER_MSG.format(serverip))
            return serverip, receivedport
        else:
            print(IMPOSTER_OFFER_MSG.format(serverip))
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

def multi_gamemode_senddata(sock):
    try:
        data = getch.getch()
        sock.send(data)
    except Exception as e:
        print(e)
    pass

def multi_gamemode_downloaddata(sock):
    try:
        data = sock.recv(BUFFER_SIZE)
        if data != "":
            data = str(data, TXT_ENCODING)
            print(data)
    except Exception as e:
        print(e)
    pass


def theloop():
    (serverip, port) = looking_for_server_state()
    tcpsocket = connect_to_server_state(serverip, port)
    if tcpsocket == None:
        print(bcolors.WARNING + FAILED_TO_CONNECT_MSG)
        theloop()
    else:
        tcpsocket.send(bytes(TEAMNAME, TXT_ENCODING))
        downloading = threading.Thread(target=multi_gamemode_downloaddata, args=(tcpsocket,))
        uploading = threading.Thread(target=multi_gamemode_senddata, args=(tcpsocket,))
        downloading.start()
        uploading.start()
        downloading.join()
        uploading.join()
        theloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    theloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
