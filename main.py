# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import threading
from random import randint
from socket import *
import time
import struct
from threading import Thread

threads = []
records = []
lock = threading.Lock()


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


class ClientThread(threading.Thread):
    def __init__(self, clientsocket, clientAddress):
        threading.Thread.__init__(self)
        self.teamname = None
        self.socket = clientsocket
        self.address = clientAddress
        self.lock = threading.Lock()
        print('New connection added: ', clientAddress)

    def run(self):
        name = str(get_input_from_player(self.socket), 'utf-8')
        self.teamname = name

    def getinput(self):
        return get_input_from_player(self.socket)

    def sendoutput(self, message):
        self.socket.send(bytes(message, 'utf-8'))


def thread_function(tcp_1):
    global threads
    tcp_1.setblocking(1)
    while len(threads) < 2:
        try:
            tcp_1.listen(2)
            (conn, addr) = tcp_1.accept()
            thread = ClientThread(conn, addr)
            thread.start()
            threads.append(thread)
        except Exception as ex:
            print(ex)
            time.sleep(1)
            for thread in threads:
                thread.socket.close()
                thread.join()
            threads = []
    return threads


def getQA():
    var = [('How much is square root of 9?', '3'), ('How much is square root of 81?', '9'),
           ('How much blonde women you need to change a light bolb', '1'),
           ('How much is 2 + 2 - 1?', '3'), ('How much is 9 square of 0?', '1')]
    value = randint(0, len(var) - 1)
    return var[value]


def opentcpcon():
    try:
        s_tcp1 = socket(AF_INET, SOCK_STREAM)
        s_tcp1.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s_tcp1.bind((gethostname(), 0))
        return s_tcp1
    except Exception as e:
        print(e)
        return -1, -1

#use struct.pack(strFormat,0xabcddbca,0x02,
def MODE_OFFER():
    global threads
    threads = []
    UDP_IP = '127.0.0.4'
    UDP_PORT = 13117
    tcp_1 = opentcpcon()
    port1 = tcp_1.getsockname()[1]
    x = threading.Thread(target=thread_function, args=(tcp_1,))
    s_udp = socket(AF_INET, SOCK_DGRAM)
    try:
        print(bcolors.HEADER + f'Server started, listening on IP address {UDP_IP}' + bcolors.ENDC)
        s_udp.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        PORT_TO_SEND = port1.to_bytes(2, 'little')
        SEND_PACKET = struct.pack('lci', 0xabcddcba, b'\x02', PORT_TO_SEND)
        x.start()
        while len(threads) < 2:
            s_udp.sendto(SEND_PACKET, ('255.255.255.255', UDP_PORT))
            time.sleep(0.5)
        s_udp.close()
        tcp_1.close()
        x.join()
    except Exception as e:
        print(e)
        tcp_1.close()
        x.join()
        threads = []
        time.sleep(0.5)
        tcp_1 = opentcpcon()
        port1 = tcp_1.getsockname()[1]
        x = threading.Thread(target=thread_function, args=(tcp_1,))
        x.start()

    (q, a) = getQA()
    gamemode(threads[0], threads[1], q, a)
    MODE_OFFER()


def get_input_from_player(t):
    try:
        return t.recv(1024)
    except:
        return ''


def gamemode(t1, t2, problem, ans):
    global records
    time.sleep(10)
    winner = 'draw'
    name1 = t1.teamname
    name2 = t2.teamname
    if name1 is not None and name2 is not None:
        welcome_message = f'Welcome to Quick Maths.  \nPlayer 1: {name1} \nPlayer 2: {name2} \n== \nPlease answer the ' \
                          f'following question as fast as you can: '
        problem = welcome_message + ' ' + problem
        t1.sendoutput(problem)
        t2.sendoutput(problem)
        t = time.time()
        while time.time() - t < 10:
            p1 = t1.getinput()
            p2 = t2.getinput()
            if p1 != '':
                p1 = str(p1, 'utf-8')
            if p2 != '':
                p2 = str(p2, 'utf-8')
            if p1 == ans:
                winner = name1
                break
            elif p2 == ans:
                winner = name2
                break
            elif p1 != '':
                winner = name2
                break
            elif p2 != '':
                winner = name1
                break
        end_message = f'Game over! \nThe correct answer was {ans}! \nCongratulations to the winner: {winner}'
        t1.sendoutput(end_message)
        t2.sendoutput(end_message)
        t1.socket.close()
        t1.join()
        t2.socket.close()
        t2.join()
    elif name1 is None and name2 is None:
        t1.socket.close()
        t1.join()
        t2.socket.close()
        t2.join()
    elif name1 is None:
        winner = name2
        end_message = f'Game over! \nThe Opponent didnt send name \nCongratulations to the winner: {winner}'
        t2.sendoutput(end_message)
        t1.socket.close()
        t1.join()
        t2.socket.close()
        t2.join()
        print('Game over, sending out offer\nrequests...')
    elif name2 is None:
        winner = name1
        end_message = f'Game over! \nThe Opponent didnt send name \nCongratulations to the winner: {winner}'
        t1.sendoutput(end_message)
        t1.socket.close()
        t1.join()
        t2.socket.close()
        t2.join()
    if winner is not 'draw':
        foundwin = False
        for r in records:
            if r[0] is winner:
                foundwin = True
                r[1] = r[1] + 1
        if not foundwin:
            records.append((winner, 1))
        loser = ''
        if winner is name1:
            loser = name2
        else:
            loser = name1
        foundlose = False
        for r in records:
            if r[0] is loser:
                foundlose = True
                r[1] = r[1] + 0
        if not foundlose:
            records.append((loser, 0))
    bestis = 'no'
    score = -1
    for r in records:
        if r[1] > score:
            score = r[1]
            bestis = r[0]
        elif r[1] is score:
            bestis = 'Tied'

    print(bcolors.OKBLUE + f'The most wins in the server is {bestis} with the score of {score}' + bcolors.ENDC)

    print('Game over, sending out offer\nrequests...')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        MODE_OFFER()
    except Exception as e:
        print(e)
