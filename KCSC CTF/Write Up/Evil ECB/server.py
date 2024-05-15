from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad, unpad
from os import urandom
import json
import socket
import threading

flag = 'KCSC{s0m3_r3ad4ble_5tr1ng_like_7his}'

menu = ('\n\n|---------------------------------------|\n' +
            '| Welcome to Evil_ECB!                  |\n' +
            '| Maybe we can change the Crypto world  |\n' +
            '| with a physical phenomena :D          |\n' +
            '|---------------------------------------|\n' +
            '| [1] Login                             |\n' +
            '| [2] Register ^__^                     |\n' +
            '| [3] Quit X__X                         |\n' +
            '|---------------------------------------|\n')

bye = ( '[+] Closing Connection ..\n'+
        '[+] Bye ..\n')

class Evil_ECB:
    def __init__(self):
        self.key = urandom(16)
        self.cipher = AES.new(self.key, AES.MODE_ECB)
        self.users = ['admin']

    def login(self, token):
        try:
            data = json.loads(unpad(self.cipher.decrypt(bytes.fromhex(token)), 16).decode())
            if data['username'] not in self.users:
                return '[-] Unknown user'

            if data['username'] == "admin" and data["isAdmin"]:
                return '[+] Hello admin , here is your secret : %s\n' % flag

            return "[+] Hello %s , you don't have any secret in our database" % data['username']
        except:
            return '[-] Invalid token !'
        
    def register(self, user):
        if user in self.users:
            return '[-] User already exists'
 
        data = b'{"username": "%s", "isAdmin": false}' % (user.encode())
        token = self.cipher.encrypt(pad(data, 16)).hex()
        self.users.append(user)
        return '[+] You can use this token to access your account : %s' % token

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        chal = Evil_ECB()
        client.send(menu.encode())
        for i in range(10):
            try:
                client.send(b'> ')
                choice = client.recv(size).strip()
                if choice == b'1':
                    client.send(b'Token: ')
                    token = client.recv(size).strip().decode()
                    client.send(chal.login(token).encode() + b'\n')
                elif choice == b'2':
                    client.send(b'Username: ')
                    user = client.recv(size).strip().decode()
                    client.send(chal.register(user).encode() + b'\n')
                elif choice == b'3':
                    client.send(bye.encode())
                    client.close()
                else:
                    client.send(b'Invalid choice!!!!\n')
                    client.close()
            except:
                client.close()
                return False
        client.send(b'No more rounds\n')
        client.close()

if __name__ == "__main__":
    ThreadedServer('',2003).listen()