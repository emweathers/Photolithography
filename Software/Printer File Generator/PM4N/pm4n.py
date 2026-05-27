import struct
from PIL import Image
import numpy as np
import os


def calc_dur():
    d = 0
    mask_list = os.listdir('./masks')
    for f in mask_list:
        d += int(f[f.find('.')+1:-4])
    return d


def generate_preview():
    image = Image.new(mode="RGB",size=(224,168),color="black")
    try:
        zero_mask = os.listdir('./masks')[0]
        if(zero_mask.startswith("0.")):
            mask = Image.open('./masks/'+zero_mask).resize((224,127),Image.Resampling.NEAREST)
            image.paste(mask,(0,20))
        else:
            print("Zero-Mask could not be found. Preview will generate blank.")
    except:
        print("Could not find masks folder. Preview will generate blank.")
    image.save("preview.bmp")
    return


def load_preview(image):
    # print("Loading preview.bmp...")
    # image = Image.open('preview.bmp')
    out = []
    if(image.width != 224 or image.height != 168):
        raise ValueError("Preview image 'preview.bmp' should have width 224 and height 168.")
    for r,g,b in image.get_flattened_data():
        rgb = struct.pack('H',(((r >> 3) & 0x1F) << 11) | (((g >> 2) & 0x3F) << 5) | ((b >> 3) & 0x1F))
        out.append(rgb)
    return out





#preview_image = np.array(load_preview(Image.open('preview.bmp')))

def BMP_to_RLE(path):
    img = Image.open(path).convert('L')
    px = list(img.get_flattened_data())
    for i in range(len(px)):
        px[i] = px[i] >> 4 # Keep only the upper portion
    out = []

    pixel = px[0]
    rl = 0

    for i in range(0,len(px)):
        if(px[i] == pixel and rl < 0x0FFF):
            rl += 1
        else:
            out.append(rl+(px[i-1] << 12)) # [Color (4-bits)][Length (12-bits)]
            pixel = px[i]
            rl = 1
    return out


def generate_pm4n(preview_image):

    mask_files = os.listdir('./masks')

    # Miscellaneous Constants and Parameters
    px_size_um = float(17)
    width = 9024
    height = 5120

    exposure_time_sec = float(10)
    grey_count = 16

    preview_table_size = 12 + (4 * 4) + 2 * preview_image.size
    layer_count = len(mask_files) #                        TODO TODO TODO TODO
    layer_table_size = 4 + layer_count * (32)
    extra_table_size = 24
    machine_table_size = 12 + 4 + 96 + 16 + (7 * 4)

    preview_table_addr = int('0x98',16)
    layer_img_addr = preview_table_addr + preview_table_size
    layer_def_addr = layer_img_addr + grey_count + 12
    extra_table_addr = layer_def_addr + (12 + 4) + layer_table_size
    machine_table_addr = (12 + 4) + extra_table_addr + extra_table_size * 2 + 2 * 4
    layer_start_addr = machine_table_addr + machine_table_size

    # Address Header Table
    address_header = [
        ("ANYCUBIC\0\0\0\0").encode(),                      # Brand Text
        (516).to_bytes(4,byteorder='little'),               # Version Number
        (8).to_bytes(4,byteorder='little'),                 # Table Quantity
        (int('0x34',16)).to_bytes(4,byteorder='little'),    # Header Table Address
        (int('0x00',16)).to_bytes(4,byteorder='little'),    # Software Table Address            (Does not exist for this model)
        (int('0x98',16)).to_bytes(4,byteorder='little'),    # Preview Table Address
        (layer_img_addr).to_bytes(4,byteorder='little'),    # Layer Image Color Table Address   (Calculated)
        (layer_def_addr).to_bytes(4,byteorder='little'),    # Layer Definition Table Address    (Calculated)
        (extra_table_addr).to_bytes(4,byteorder='little'),  # Extra Table Address               (Calculated)
        (machine_table_addr).to_bytes(4,byteorder='little'),# Machine Table Address             (Calculated)
        (layer_start_addr).to_bytes(4,byteorder='little'),  # Layer Start Address               (Calculated)
    ]


    # Header Table
    header = [
        ("HEADER\0\0\0\0\0\0").encode(),                    # Header Text
        (84).to_bytes(4,byteorder='little'),                # Header Table Size
        struct.pack('f',px_size_um),                        # Pixel Size in μm
        struct.pack('f',1),                                 # Layer Thickness in mm
        struct.pack('f',exposure_time_sec),                 # Exposure Time in Seconds
        struct.pack('f',-7),                                # Off Time in Seconds
        struct.pack('f',0),                                 # Bottom Layer Exposure Time
        struct.pack('f',0),                                 # Bottom Layer Count
        struct.pack('f',0),                                 # Lift Distance in mm
        struct.pack('f',100),                               # Lift Speed in mm/s
        struct.pack('f',100),                               # Retract Speed in mm/s
        struct.pack('f',0),                                 # Volume in mL
        (1).to_bytes(4,byteorder='little'),                 # Anti-Aliasing Setting
        width.to_bytes(4,byteorder='little'),               # Screen Width
        height.to_bytes(4,byteorder='little'),              # Screen Height
        struct.pack('f',0),                                 # Weight in Grams
        struct.pack('f',-1),                                # Price
        ("$\0\0\0").encode(),                               # Currency Symbol
        (1).to_bytes(4,byteorder='little'),                 # Per-Layer Override
        (-1).to_bytes(4,byteorder='little',signed=True),    # Estimated Time in Seconds
        (0).to_bytes(4,byteorder='little'),                 # Transition Layer Count
        (0).to_bytes(4,byteorder='little'),                 # Transition Layer Type
        (1).to_bytes(4,byteorder='little'),                 # Advanced Mode
    ]


    # Image Preview Table
    preview = [
        ("PREVIEW\0\0\0\0\0").encode(),
        (preview_table_size).to_bytes(4,byteorder='little'),
        (224).to_bytes(4,byteorder='little'),
        ("x\0\0\0").encode(),
        (168).to_bytes(4,byteorder='little'),
        preview_image.tobytes()
    ]


    # Grey Table
    grey_table = [
        (int(0)).to_bytes(4,byteorder='little'),            # Use Greyscale (Boolean)
        (int(grey_count)).to_bytes(4,byteorder='little'),   # Number of Grey colors (from 0 to 16)
        (int(0)).to_bytes(grey_count,byteorder='little'),   # Grey color assignment
        (int(0)).to_bytes(4,byteorder='little')             # Unknown
    ]


    # Layer Definition Table
    layer_def_table = [
        
    ]


    with open("test.pm4n","wb") as f:
        for b in address_header:
            f.write(b)
        for b in header:
            f.write(b)
        for b in preview:
            f.write(b)
        for b in grey_table:
            f.write(b)
        f.close()
    
    return



def main():
    generate_preview()
    preview_image = np.array(load_preview(Image.open('preview.bmp')))
    generate_pm4n(preview_image)

main()