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