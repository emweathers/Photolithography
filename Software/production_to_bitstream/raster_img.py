from PIL import Image
import numpy as np
import os

def raster_bitstream(w,h,path='./'):
    name_list = []
    image_list = []
    color_list = []

    for file in os.listdir(path): # Check through all files in path
        # Acquire filename and extension
        name, extension = os.path.splitext(file)

        if(extension.lower() in (".bmp",".jpg",".jpeg",".png")):
            # Open image as grayscale image
            img = Image.open(path+"/"+file).convert('L')
            
            if(w != img.width or h != img.height):
                print(f"Mismatched Dimensions between image {file} and specified dimensions.")
            else:
                # Get colors
                img_array = np.array(img)
                colors = np.unique(img_array)

                # Append file name, raster image data, and colors to output lists
                name_list.append(name)
                image_list.append(img)
                color_list.append(colors)
    
    return name_list,image_list,color_list

if __name__ == "__main__":
    a,b,c = raster_bitstream(9024,5120,"Test Project/masks")
    print(c)