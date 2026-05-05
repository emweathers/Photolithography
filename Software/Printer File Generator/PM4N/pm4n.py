import struct
from PIL import Image



preview_image = []

def load_preview():
    print("Loading preview.bmp...")
    image = Image.open('preview.bmp')
    if(image.width != 224 or image.height != 168):
        raise ValueError("Preview image 'preview.bmp' should have width 224 and height 168.")
    
    return

load_preview()


# Miscellaneous Constants and Parameters
px_size_um = float(17)
width = 9024
height = 5120

exposure_time_sec = float(10)
grey_count = 16


# Address Header Table
address_header = [
    ("ANYCUBIC\0\0\0\0").encode(),                      # Brand Text
    (516).to_bytes(4,byteorder='little'),               # Version Number
    (8).to_bytes(4,byteorder='little'),                 # Table Quantity
    (int('0x34',16)).to_bytes(4,byteorder='little'),    # Header Table Address
    (int('0x00',16)).to_bytes(4,byteorder='little'),    # Software Table Address            (Does not exist for this model)
    (int('0x98',16)).to_bytes(4,byteorder='little'),    # Preview Table Address
    (int('0x00',16)).to_bytes(4,byteorder='little'),    # Layer Image Color Table Address   (Calculated)
    (int('0x00',16)).to_bytes(4,byteorder='little'),    # Layer Definition Table Address    (Calculated)
    (int('0x00',16)).to_bytes(4,byteorder='little'),    # Extra Table Address               (Calculated)
    (int('0x00',16)).to_bytes(4,byteorder='little'),    # Machine Table Address             (Calculated)
    (int('0x00',16)).to_bytes(4,byteorder='little'),    # Layer Start Address               (Calculated)
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
    (int('0x00',16)).to_bytes(4,byteorder='little'),
    (224).to_bytes(4,byteorder='little'),
    ("x\0\0\0").encode(),
    (168).to_bytes(4,byteorder='little'),
]


with open("test.pm4n","wb") as f:
    for b in address_header:
        f.write(b)
    for b in header:
        f.write(b)
    for b in preview:
        f.write(b)
    f.close()

