import streamlit as sl 
from rembg import remove
from io import BytesIO
from PIL import Image, ImageOps
import base64

sl.set_page_config(layout="wide", page_title="Remove Background From Any Image")
sl.write("## Remove Background From any Image")
sl.write()
sl.sidebar.write("## Upload and Download :gear:")
Max_file_Size = 5 * 1024 * 1024

def convert_img(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    bytes_im = buf.getvalue()
    return bytes_im

def fix_image(upload, bg_color, bg_color_name):
    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)

    fixed = remove(image)
    
    if bg_color_name == "No Background":
        result_image = fixed
    else:
        # Create a background with the selected color
        bg = Image.new("RGBA", fixed.size, bg_color)
        result_image = Image.alpha_composite(bg, fixed)
    
    col2.write(f"Fixed Image with {bg_color_name} Background :wrench:")
    col2.image(result_image)
    
    sl.sidebar.markdown("\n")
    sl.sidebar.download_button("Download the Image", convert_img(result_image), "fixed.png", "image/png")

col1, col2 = sl.columns(2)

# Sidebar for file upload and background color selection
my_upload = sl.sidebar.file_uploader("Upload an Image Here", type=["png", "jpg", "jpeg"])
bg_color_name = sl.sidebar.selectbox("Choose Background Color", ["No Background", "white", "yellow", "blue"])

# Convert color name to RGBA value
bg_color_dict = {
    "white": (255, 255, 255, 255),
    "yellow": (255, 255, 0, 255),
    "blue": (0, 0, 255, 255)
}
selected_bg_color = bg_color_dict.get(bg_color_name, None) 

if my_upload is not None:
    if my_upload.size > Max_file_Size:
        sl.error("The file size is larger than 5MB.")
    else:
        fix_image(upload=my_upload, bg_color=selected_bg_color, bg_color_name=bg_color_name)
else:
    fix_image("./givefile.png", bg_color=selected_bg_color, bg_color_name=bg_color_name)
