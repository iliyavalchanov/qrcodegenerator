import qrcode
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

# Google Forms URL for "My top 3 AI assistants"
url = 'https://docs.google.com/forms/d/e/1FAIpQLSf3K_QXXMOesgXi2qteXWcLjgw5noUT1hUgNfCl0lFfwxeoBA/viewform?usp=header'

# Generate QR code with rounded/circular modules
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# Create QR code image with circular modules
qr_img = qr.make_image(
    fill_color="black",
    back_color="white",
    image_factory=StyledPilImage,
    module_drawer=CircleModuleDrawer(),
    color_mask=SolidFillColorMask()
).convert('RGB')

# Load logo image
logo = Image.open('powerofbg.jpeg')

# Resize logo
qr_width, qr_height = qr_img.size
logo_size = int(qr_width * 0.25)
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

# Paste logo in the center
pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

# Save result
qr_img.save('pobg-quiz.png')
print('Beautiful QR code for AI assistants quiz saved as pobg-quiz.png') 