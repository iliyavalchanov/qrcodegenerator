from http.server import BaseHTTPRequestHandler
import json
import qrcode
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
import io
import base64

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            url = data.get('url', '')
            logo_data = data.get('logo', None)
            
            if not url:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'URL is required'}).encode())
                return
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            qr_img = qr.make_image(
                fill_color="black",
                back_color="white",
                image_factory=StyledPilImage,
                module_drawer=CircleModuleDrawer(),
                color_mask=SolidFillColorMask()
            ).convert('RGB')
            
            # Add logo if provided
            if logo_data:
                try:
                    logo_bytes = base64.b64decode(logo_data.split(',')[1])
                    logo = Image.open(io.BytesIO(logo_bytes))
                    
                    qr_width, qr_height = qr_img.size
                    logo_size = int(qr_width * 0.25)
                    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
                    
                    pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                    qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
                except Exception as e:
                    pass  # Continue without logo if there's an error
            
            # Convert to base64
            buf = io.BytesIO()
            qr_img.save(buf, format='PNG')
            buf.seek(0)
            img_base64 = base64.b64encode(buf.getvalue()).decode()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': True,
                'image': f'data:image/png;base64,{img_base64}'
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 