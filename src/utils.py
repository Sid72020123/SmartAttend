import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image


def make_qrcode(url: str):
    qr = qrcode.QRCode(
        version=None,  # Automatically choose the QR version
        error_correction=ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)

    qr_image = qr.make_image(
        fill_color="#111827",
        back_color="white",
    ).convert("RGB")

    logo = Image.open("src/static/images/logo.png").convert("RGBA")

    # Keep the logo small
    max_logo_size = qr_image.width // 6
    logo.thumbnail((max_logo_size, max_logo_size))

    # Place a white background behind the logo
    padding = 8

    background = Image.new(
        "RGBA",
        (logo.width + padding * 2, logo.height + padding * 2),
        "white",
    )

    background.alpha_composite(logo, (padding, padding))

    # Check that the logo fits
    # if background.width >= qr_image.width // 3:
    #     raise ValueError("Logo is too large for this QR code")

    # Center the logo
    position = (
        (qr_image.width - background.width) // 2,
        (qr_image.height - background.height) // 2,
    )

    qr_image.paste(background.convert("RGB"), position)

    return qr_image
