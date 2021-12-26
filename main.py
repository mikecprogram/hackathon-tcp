# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import threading
from random import randint
from socket import *
import time
from _thread import *
from threading import *

USERS = 0


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


class ClientThread(Thread):

    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print
        "[+] New server socket thread started for " + ip + ":" + str(port)

    def run(self):
        while True:
            data = conn.recv(2048)
            print
            "Server received data:", data
            MESSAGE = raw_input("Multithreaded Python server : Enter Response from Server/Enter exit:")
            if MESSAGE == 'exit':
                break
            conn.send(MESSAGE)  # echo

    def getName(self, client):
        size = 1024
        while True:
            try:
                name = str(get_input_from_player(client), 'utf-8')
                if name:
                    return name
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False


def getQA():
    var = [("How much is 2 + 2?", "4"), ("How much is 2 + 3?", "5"),
           ("How much is square root of 9?", "3"), ("How much is square root of 81?", "9"),
           ("How much blonde women you need to change a light bolb", "1"),
           ("How much is 2 + 2 - 1?", "3"), ("How much is 9 square of 0?", "1")]
    value = randint(0, len(var) - 1)
    return var[value]


def threadtcp(tcpsock):
    return tcpsock + 1


def opentcpcon():
    try:
        s_tcp1 = socket(AF_INET, SOCK_STREAM)
        s_tcp1.setblocking(0)
        s_tcp1.bind((gethostname(), 0))
        SIGN_PORT = s_tcp1.getsockname()[1]
        s_tcp1.listen(2)
        return SIGN_PORT, s_tcp1
    except Exception as e:
        print(e)
        return -1, -1


def sendmessagebothtcp(t1, t2, message):
    t1.send(bytes(message, 'utf-8'))
    t2.send(bytes(message, 'utf-8'))


def MODE_OFFER():
    UDP_IP = '127.0.0.4'
    UDP_PORT = 13117
    MESSAGE = 'Server started, listening on IP address'

    port1 = -1
    while port1 == -1:
        port1 = thread1.sock.getsockname()[1]
    conn1 = 0
    conn2 = 0
    name1 = 'n1'
    name2 = 'n2'
    try:
        s_udp = socket(AF_INET, SOCK_DGRAM)
        print(f'Server started, listening on IP address {UDP_IP}')
        s_udp.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        PORT_TO_SEND = port1.to_bytes(2, 'little')
        SEND_PACKET = b'\xab\xcd' + b'\xdc\xba\x02' + PORT_TO_SEND
        while True:
            s_udp.sendto(SEND_PACKET, ('255.255.255.255', UDP_PORT))
            try:
                if conn1 == 0:
                    thread1.listen(1)
                    conn1 = thread1.sock
                    print('player 1 connected')
                    name1 = thread1.getName(conn1)

                elif conn2 == 0:
                    thread2 = ThreadedServer('', UDP_PORT)
                    thread2.listen(1)
                    conn2 = thread2.sock
                    print("player 2 connected")
                    name1 = thread2.getName(conn2)
                    s_udp.close()
                    break
            except Exception as e:
                time.sleep(1)

    except Exception as e:
        print(e)
    (q, a) = getQA()
    gamemode(conn1, conn2, name1, name2, q, a)


def get_input_from_player(t):
    try:
        return t.recv(1024)
    except:
        return ""


def gamemode(t1, t2, name1, name2, problem, ans):
    # time.sleep(10)
    winner = "draw"
    welcome_message = f'Welcome to Quick Maths.  \nPlayer 1: {name1} \nPlayer 2: {name2} \n== \nPlease answer the ' \
                      f'following question as fast as you can: '
    problem = welcome_message + " " + problem
    sendmessagebothtcp(t1, t2, problem)
    t = time.time()
    t1.setblocking(0)
    t2.setblocking(0)
    while time.time() - t < 10:
        p1 = get_input_from_player(t1)
        p2 = get_input_from_player(t2)
        if p1 == ans:
            winner = name1
            break
        elif p2 == ans:
            winner = name2
            break
        elif p1 != "":
            winner = name2
            break
        elif p2 != "":
            winner = name1
            break
    end_message = f'Game over! \nThe correct answer was {ans}! \nCongratulations to the winner: {winner}'
    sendmessagebothtcp(t1, t2, end_message)
    t1.close()
    t2.close()
    print("“Game over, sending out offer\nrequests...”")
    MODE_OFFER()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        MODE_OFFER()
    except Exception as e:
        print(e)
