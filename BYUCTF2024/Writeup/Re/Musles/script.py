s=""
with open("data","r") as f:
    for i in f:
        data = int(i,16)^0x20
        tmp = hex(data)[2:]
        s+=tmp.zfill(2)
print(s)
