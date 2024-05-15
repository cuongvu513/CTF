import json
from pwn import *
from Crypto.Util.Padding import pad, unpad

io = remote("103.163.24.78",2003)
print(io.recv().decode())

def login(token):
    global io
    io.recv().decode()
    io.sendline('1'.encode())
    io.recv().decode()
    io.sendline(token.encode())
    print(io.recv().decode())

data = b'{"username": "admin", "isAdmin": true}'
data = b"xx"+ pad(data,16) +b"x"

def reg(user):
    global io
    io.recv().decode()
    io.sendline('2'.encode())
    io.recv().decode()
    io.sendline(user)
    data = (io.recv().decode())
    return data[data.index(":")+2:]
print(login(reg(data)[32:128]))




