from PIL import Image
import os

def raster_bitstream(path='./'):
    image_list = []
    for file in os.listdir(path): # Check through all files in path
        # Acquire filename and extension
        name, extension = os.path.splitext(file)

        if(extension.lower() in (".bmp",".jpg",".jpeg",".png")):
            # Open image as grayscale image
            img = Image.open(path+"/"+file).convert('L')

            # Append tuple of file name and raster image data to output image list
            image_list.append((name,img))
    
    return image_list

if __name__ == "__main__":
    print(raster_bitstream("Test Project/masks"))