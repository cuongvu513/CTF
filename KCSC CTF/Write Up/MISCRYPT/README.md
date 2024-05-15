Ở trong challenge có 2 file python: 1 file tạo ra qr và 1 file là mã hóa qr.

Tạm thời đọc qua file gen_qr_flag.py chúng ta thấy chỉ là tạo ra qr và không có gì đặc biệt.

Sang đến file chall.py 

```python
from PIL import Image
import numpy as np
import galois
GF256 = galois.GF(2**8)

img = Image.open('qr_flag_rgb.png')
pixels = img.load()
width, height = img.size

M = GF256(np.random.randint(0, 256, size=(3, 3), dtype=np.uint8))

# scan full height -> weight
for x in range(width):
    for y in range(0,height,3):
        A = GF256([pixels[x, y], pixels[x, y+1], pixels[x, y+2]])
        M = np.add(A, M)
        pixels[x, y], pixels[x, y+1], pixels[x, y+2] = [tuple([int(i) for i in j]) for j in M]
        
img.save('qr_flag_encrypt.png')
```
Cách mã hóa ở đây là tạo ra một ma trận M ngẫu nhiên, tiếp đến sẽ mã hóa theo cách sau:
```python
for x in range(width):
    for y in range(0,height,3):
        A = GF256([pixels[x, y], pixels[x, y+1], pixels[x, y+2]])
        M = np.add(A, M)
        pixels[x, y], pixels[x, y+1], pixels[x, y+2] = [tuple([int(i) for i in j]) for j in M]
```
Ở đây A sẽ là các ma trận điểm ảnh sau đó bị thay thế bởi M+A và M= M+A. Việc này lặp lại đến hết chiều dài, chiều rộng của bức ảnh. 

Vì thế để giải mã ta chỉ cần làm ngược lại, ma trận ở vị trí I sẽ bằng I trừ đi ma trận trước nó.

Nên ta chỉ cần vị trí trước nó rồi trừ đi là được.

```python
from PIL import Image
import numpy as np
import galois
GF256 = galois.GF(2**8)
img = Image.open('qr_flag_encrypt.png')

pixels = img.load()
width, height = img.size
print(height,width)
# tìm vị trí ma trận đằng trước ma trận hiện tại 
def pre(x,y):
    if (y-3<0): 
        y = (y-3)%999
        x = x-1
    else: y -= 3
    global GF256, pixels
    return  GF256([pixels[x, y], pixels[x, y+1], pixels[x, y+2]])
# Đi ngược từ cuối về đầu
for x in range(width-3,-1,-1):
    for y in range(height-3,-1,-3):
        A = GF256([pixels[x, y], pixels[x, y+1], pixels[x, y+2]])
        M = pre(x,y)
        M = np.subtract(A, M)
        pixels[x, y], pixels[x, y+1], pixels[x, y+2] = [tuple([int(i) for i in j]) for j in M]
img.save('qr_flag.png')  
```
Sau khi quét QR chúng ta sẽ ra được flag 

