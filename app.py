import gradio as gr
import qrcode
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer,
    GappedSquareModuleDrawer, 
    CircleModuleDrawer,
    RoundedModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer
)
from qrcode.image.styles.colormasks import SolidFillColorMask
import io

# Style mapping for module drawers
STYLE_MAP = {
    'Square': SquareModuleDrawer,
    'Gapped Square': GappedSquareModuleDrawer,
    'Circle': CircleModuleDrawer,
    'Rounded': RoundedModuleDrawer,
    'Vertical Bars': VerticalBarsDrawer,
    'Horizontal Bars': HorizontalBarsDrawer
}

def generate_qr(data, logo_file, style):
    if not data:
        return None
    
    # Get the appropriate module drawer
    module_drawer_class = STYLE_MAP.get(style, CircleModuleDrawer)
    module_drawer = module_drawer_class()
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(
        fill_color="black",
        back_color="white",
        image_factory=StyledPilImage,
        module_drawer=module_drawer,
        color_mask=SolidFillColorMask()
    ).convert('RGB')
    if logo_file is not None:
        logo = Image.open(logo_file)
        qr_width, qr_height = qr_img.size
        logo_size = int(qr_width * 0.25)
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
    buf = io.BytesIO()
    qr_img.save(buf, format='PNG')
    buf.seek(0)
    return gr.Image.update(value=buf, label="Your QR Code"), buf

def main():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown("# <span style='color:#ff5ecb'>QR Code Studio</span>", unsafe_allow_html=True)
        gr.Markdown("Create stunning QR codes with your custom logo and style")
        with gr.Row():
            with gr.Column():
                url = gr.Textbox(label="URL or Text", placeholder="https://example.com")
                style = gr.Dropdown(
                    label="QR Code Style",
                    choices=list(STYLE_MAP.keys()),
                    value="Circle",
                    interactive=True
                )
                logo = gr.File(label="Upload Logo (PNG, JPG, SVG)", file_types=["image"])
                btn = gr.Button("Generate Beautiful QR Code")
            with gr.Column():
                qr_img = gr.Image(label="Preview & Download", interactive=False)
                download = gr.File(label="Download QR Code")
        btn.click(fn=generate_qr, inputs=[url, logo, style], outputs=[qr_img, download])
    demo.launch()

if __name__ == "__main__":
    main() 