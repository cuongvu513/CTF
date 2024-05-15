import qrcode
from PIL import Image

# Define the text you want to encode
text = "flag hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"

# Generate the QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=1,
    border=1,
)

# Add the data to the QR code
qr.add_data(text)
qr.make(fit=True)

# Create an image from the QR code
img = qr.make_image(fill_color="black", back_color="white")

# Resize the image to the desired size
img = img.resize((999, 999), resample=Image.NEAREST)

# Convert the image to RGB mode
img = img.convert("RGB")

# Create a new image with RGB values for each pixel
new_img = Image.new("RGB", img.size)

# Iterate over each pixel and set RGB values
for x in range(img.width):
    for y in range(img.height):
        r, g, b = img.getpixel((x, y))
        new_img.putpixel((x, y), (r, g, b))

# Save the image
new_img.save("qr_flag_rgb.png")