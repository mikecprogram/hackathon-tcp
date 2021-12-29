# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from random import randint
from socket import *
import struct
import time
from multiprocessing import *
import select

records = []
BROADCASTIP = '255.255.255.255'
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
    YELLOW = '\033[33m'
MSG_NOANSWER = bcolors.FAIL+'No one answered!'+bcolors.ENDC
MSG_CORRECT = bcolors.YELLOW+'{} was correct! -> {}'+bcolors.ENDC
MSG_WRONG = bcolors.FAIL+'{} was wrong.. -> {}'+bcolors.ENDC
COOKIE = 0xabcddcba
OP_OFFER = 0x02
# question pool chhose one randomly
def getQA():
    var = [('If there are four apples and you take away three, how many do you have?', '3'),
           (
               'A 300 ft. train is traveling 300 ft. per minute must travel through a 300 ft. long tunnel. How long '
               'will it take the train to travel through the tunnel?(in minutes)', '2'),
           ('How much is square root of 9?', '3'),
           ('How much is square root of 81?', '9'),
           ('How many prime numbers are between 4 and 12?', '3'),
           ('2 plus 2, minus 2 ,devided by 2 is..?', '1'),
           ('What number can you write using only one line?', '1'),
           ('How much is half of 8?', '4'),
           ('Four out of Five ducks drowned in the river, how many left? (Can they even drown?) ', '5'),
           ('If I baked 11 cookies, and I ate 3, burned 4 and hid 1, how many cookies left for my friends?', '3'),
           ('How much blonde women you need to change a light bolb?', '1'),
           ('How much is 2 + 2 - 1?', '3'),
           ('How many generals are in the Two Generals problem?', '2'),
           ('What is the meaning of life?(Sum the digits pls)', '6'),
           ('How many slices there are in a normal sliced pizza?', '8'),
           ('How I met your mother?', '9'),
           ('What is the newest version of IP protocol?', '6'),
           ('How many calls can you make from three cellphones, when one of them is out of service and the other have two sims inside?', '3'),
           ('How many apples a day can keep the doctor away?','1'),
           ('How many numbers from 0 to 9 contain circles in them?','4'),
           ('Which number contains two circles in each?','8'),

           (
               'A grandmother, two mothers, and two daughters went to a baseball game together and bought one ticket '
               'each. How many tickets did they buy in total?',
               '3'),
           ('The six digit number 54321A is divisible by 9 where A is a single digit whole number. Find A.', '3'),
           (
               'Choose a number from 1 to 20. Double it, add 10, divide by 2, and then subtract the number you '
               'started with',
               '5'),
           (
               'A farmer has 19 sheep on his land. One day, a big storm hits, all but seven ran away. How many '
               'sheep does the farmer have now?',
               '7')]
    value = randint(0, len(var) - 1)
    return var[value]

# opens tcp connection to receive accepts
def opentcpcon():
    try:
        s_tcp1 = socket(AF_INET, SOCK_STREAM)
        s_tcp1.setblocking(0)
        s_tcp1.bind((gethostname(), 0))
        s_tcp1.listen(2)
        SIGN_PORT = s_tcp1.getsockname()[1]
        return SIGN_PORT, s_tcp1
    except Exception as ex:
        print(ex)
        return -1, -1


def MODE_OFFER():
    UDP_PORT = 13117
    port1 = -1
    tcp_1 = socket(AF_INET, SOCK_STREAM)
    (port1, tcp_1) = opentcpcon()
    hostname = gethostname()
    UDP_IP = gethostbyname(hostname)
    conn1 = 0
    conn2 = 0
    name1 = ''
    name2 = ''
    try:
        s_udp = socket(AF_INET, SOCK_DGRAM)
        print(bcolors.HEADER+ f'Server started, listening on IP address {UDP_IP} port {port1}'+bcolors.ENDC)
        s_udp.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        # PORT_TO_SEND = port1.to_bytes(2, 'little')
        # SEND_PACKET = b'\xab\xcd' + b'\xdc\xba\x02' + PORT_TO_SEND
        while True:
            s_udp.sendto(struct.pack('IbH',COOKIE,OP_OFFER, port1), (BROADCASTIP, UDP_PORT))
            try:  # Try to connect to a player, if no players are seen - exception and keep on posting udp
                (conn, addr) = tcp_1.accept()
                if conn1 == 0:
                    conn1 = conn
                    name1 = str(get_input_from_player(conn1), 'utf-8')
                    print(bcolors.OKGREEN+name1+' connected'+bcolors.ENDC)
                elif conn2 == 0:
                    try:  # try to read from client1
                        conn1.setblocking(0)
                        data = conn1.recv(1024)
                        # if success reading: client notified us about its death
                        print(bcolors.FAIL+name1+' disconnected'+bcolors.ENDC)
                        conn1 = conn
                        name1 = str(get_input_from_player(conn1), 'utf-8')
                        print(bcolors.OKGREEN+name1+' connected'+bcolors.ENDC)
                        name1 = str(get_input_from_player(conn1), 'utf-8')
                    except:  # if exception: client is alive, and did not say anything
                        conn1.setblocking(1)
                        conn2 = conn
                        name2 = str(get_input_from_player(conn2), 'utf-8')
                        print(bcolors.OKGREEN+name2+'  connected'+bcolors.ENDC)
                        s_udp.close()
                        gamemode(conn1, conn2, name1, name2)
                        # tcp_1.close()
                        break


            except Exception as e:
                time.sleep(1)

    except Exception as e:
        print(bcolors.FAIL + 'Oh no! Something went wrong while trying to connect to one of the players \n')
        print(e)
        print(bcolors.ENDC)
    MODE_OFFER()


def get_input_from_player(t):
    try:
        return t.recv(1024)
    except:
        return ''

def tcpreadfromplayer(tcpsocket, pipe, player):
    try:
        while True:
            data = tcpsocket.recv(1024)
            data = str(data, 'utf-8')
            pipe.send(data)
    except:
        pass

# main game plan
def gamemode(t1, t2, name1, name2):
    global records
    r1, w1 = Pipe(duplex=False)
    r2, w2 = Pipe(duplex=False)
    (problem, ans) = getQA()
    winner = 'draw'
    time.sleep(10)
    welcome_message = f'Welcome to Quick Maths.  \nPlayer 1: {name1} \nPlayer 2: {name2} \n== \nPlease answer the ' \
                      f'following question as fast as you can: '
    problem = welcome_message + ' ' + problem
    t1.send(bytes(problem, 'utf-8'))
    t2.send(bytes(problem, 'utf-8'))
    # read from each client
    cli1 = Process(target=tcpreadfromplayer, args=(t1, w1, name1,))
    cli2 = Process(target=tcpreadfromplayer, args=(t2, w2, name2,))
    cli2.start()
    cli1.start()

    i, o, e = select.select([r1,r2], [], [], 10)

    p1ans = '.'
    p2ans = '.'

    if (i):
        if r1.poll():
            p1ans = r1.recv()
            if p1ans == ans:
                winner = name1
                print(MSG_CORRECT.format(name1,p1ans))
            elif p1ans != '':
                winner = name2
                print(MSG_WRONG.format(name1,p1ans))
        elif r2.poll():
            p2ans = r2.recv()
            if p2ans == ans:
                print(MSG_CORRECT.format(name2,p2ans))
                winner = name2
            elif p2ans != '':
                winner = name1
                print(MSG_WRONG.format(name2,p2ans))
    else:
        print(MSG_NOANSWER)
    # now after 10 seconds pass or two players finished to send their answers :
    # w1.close()
    # w2.close()
    # r1.close()
    # r2.close()
    cli1.terminate()
    cli2.terminate()

    
    

    end_message = f'Game over! \nThe correct answer was {ans}! \nCongratulations to the winner: {winner}'
    t1.send(bytes(end_message, 'utf-8'))
    t2.send(bytes(end_message, 'utf-8'))
    t1.close()
    t2.close()
    # adding to records
    if winner != 'draw':
        foundwin = False
        for r in records:
            if r[0] == winner:
                foundwin = True
                r[1] = r[1] + 1
        if not foundwin:
            records.append([winner, 1])
        loser = ''
        if winner == name1:
            loser = name2
        else:
            loser = name1
        foundlose = False
        for r in records:
            if r[0] == loser:
                foundlose = True
                r[1] = r[1] + 0
        if not foundlose:
            records.append([loser, 0])
        # printing the group with the most wins in the server
        bestis = 'no'
        score = -1
        for r in records:
            if r[1] > score:
                score = r[1]
                bestis = r[0]
            elif r[1] == score:
                bestis = 'Tied'
        print(
            bcolors.OKBLUE + f'The group with the most wins in the server is {bestis} with the score of {score}' + bcolors.ENDC)

    print(bcolors.OKCYAN + 'Game over,\nsending out offer requests...' + bcolors.ENDC)
    MODE_OFFER()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        MODE_OFFER()
    except Exception as e:
        print(e)
