# !!! Спершу потрібно запустити сервер потім решту !!!

import socket
import time

host = socket.gethostbyname(socket.gethostname())
port = 9090

clients = []
name = []
data_lin = ''
data_join = ''
data_xy = ''
goal = '0'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

exits = False

print('--- [ Server ] ---')
print(f'IP :: {host}\n')
print('[ Server Started ]')

while not exits:
    try:
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')

        # ---Визначення типа повідомлення---
        if '$' in data:  # $ - вказуєтся тільки під час передачі координат
            mes = True
        elif '&' in data:   # & - вказуєтся тільки під час передачі повідомлення про гол
            mes = None
        else:
            mes = False
        # ----------------------------------

        # ---Обробітка прийнятих даних---
        if mes is True:  # Обробіток координат
            good = True
            data_lin = data.split('$')
            data_xy = f'{data_lin[1]}${data_lin[2]}'                # [0] - map | [1] - x | [2] - y
            data = data_lin[0] + data_lin[1] + ' ; ' + data_lin[2]  # map = '[Ball -> Gamer1/2] :: '
        elif mes is False:   # Обробіток підключень                 # map = '[Gamer1/2 -> Ball] :: '
            good = False
            name.append(data)
        else:   # Обробіток повідомлення про гол
            good = None
            data_lin = data.split('&')          # [0] - map | [1] - '!Goal to Gamer1/2!'
            data = data_lin[0] + data_lin[1]    # map = '[Ball -> Goal_g1/2] :: '
            if data_lin[0] == '[Ball -> Goal_g1] :: ':
                goal = '1'
            elif data_lin[0] == '[Ball -> Goal_g2] :: ':
                goal = '2'
        # -------------------------------

        if addr not in clients:
            clients.append(addr)

        itsatime = time.strftime('%Y-%m-%d-%H.%M.%S', time.localtime())

        # ---Виведення даних на сервері---
        print('['+addr[0]+']=['+str(addr[1])+']=['+itsatime+']/', end='')
        if mes is True:  # Виведення координат
            print(data)
        elif mes is False:   # Виведення підключень
            print('[' + data + ']' + ' => join')
            if len(name) == 3:  # Якщо всі три частини підключені
                print('---All connecting---')
        else:
            print(data)
        # --------------------------------

        # ---Розсилання даних---
        if good is True:    # Надсилання координат та інф. про гол
            # Надсилання даних про перемвщення
            if data_lin[0] == '[Ball -> Gamer1] :: ':
                s.sendto(data_xy.encode('utf-8'), clients[name.index('g1.py')])
            elif data_lin[0] == '[Ball -> Gamer2] :: ':
                s.sendto(data_xy.encode('utf-8'), clients[name.index('g2.py')])
            elif data_lin[0] == '[Gamer1 -> Ball] :: ' or data_lin[0] == '[Gamer2 -> Ball] :: ':
                s.sendto(f'{data_lin[0]}${data_xy}'.encode('utf-8'), clients[name.index('ball.py')])
        elif good is None:     # Надсилання повідомлення про гол
            if data_lin[0] == '[Ball -> Goal_g1] :: ':
                s.sendto(goal.encode('utf-8'), clients[name.index('ball.py')])
                s.sendto(goal.encode('utf-8'), clients[name.index('g2.py')])
            elif data_lin[0] == '[Ball -> Goal_g2] :: ':
                s.sendto(goal.encode('utf-8'), clients[name.index('ball.py')])
                s.sendto(goal.encode('utf-8'), clients[name.index('g1.py')])
        elif good is False:   # Надсилання повідомлення про підключення
            message_1 = '------- [ You join ] -------\n'
            message_2 = '---MAP---'
            data_join = f'{message_1}{message_2}'.encode('utf-8')
            s.sendto(data_join, addr)
        # -----------------------
        # print('data_lin')
        data = ''
        data_lin = []
        mes = ''
        good = ''
    except:
        print('\n[ Server Stopped ]')
        exits = True

s.close()
