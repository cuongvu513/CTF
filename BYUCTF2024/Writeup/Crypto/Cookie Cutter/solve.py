import base64

cookie ="igTdKhoT0Nq7JgwqfeZv0Agk8xEDIPNBzLxU/J4GiwaiInXkp721S9fDB2RJJlPllLZxO/z7LELFE6EyTXxG9A=="
data = base64.b64decode(cookie)[16:32]
cookie ="GL6quWnT3WdBFYqa3QJpCOVsRQap8ZojGk7KOp5P2b6B4cO2+HHdULlOL8+D3o8+"
data2= base64.b64decode(cookie)[:-16]
flag = data2+data
print(base64.b64encode(flag))