import argparse
import os

# source: https://gist.github.com/LouisdeBruijn/8f41932eb218677e98d85d579c5df83d#file-argparse-py
def parse_arguments():
    """Read arguments from a command line."""
    parser = argparse.ArgumentParser(description='Modify collection of images to be Instagram-compatible')
    parser.add_argument("imgs", nargs = '+', metavar='filename',
        help='image file')

    args = parser.parse_args()
    
    return args

from PIL import Image, ImageFilter, ImageOps

def main():
    
    os.mkdir('./Processed')
    imgs = []
    for pic in args.imgs:
        img = Image.open(pic)
        imgtemp = ImageOps.exif_transpose(img)
        imgtemp.filename = img.filename
        imgs.append(imgtemp)
    ratiosum = sum([x.size[0]/x.size[1]/len(imgs) for x in imgs])
    if ratiosum < 9/10:
        endratio = 4/5 # Make all pictures 4:5        
    elif ratiosum > 25/18: 
        endratio = 16/9 # Make all images 16:9
    else: 
        endratio = 1 # make all images 1:1
        
    for img in imgs:
        if img.size[0]/img.size[1]/endratio < 1:
            kh=1 # keep height
        else:
            kh=0
                    
        ratiodiff = max([img.size[0]/img.size[1]/endratio, endratio/(img.size[0]/img.size[1])])
        
        
        if ratiodiff == 1: # do nothing
            finalimg = img
        else:
            blurimg = img.resize((int(img.size[0]*ratiodiff), int(img.size[1]*ratiodiff)))
            blurimg = blurimg.filter(ImageFilter.GaussianBlur(40))
            blurimg = blurimg.crop((round((1-kh)*((ratiodiff-1)/2*img.size[0])),
             round(kh*((ratiodiff-1)/2*img.size[1])),
             round((1-kh)*((ratiodiff+1)/2*img.size[0]) + kh*(ratiodiff*img.size[0])),
             round((kh)*((ratiodiff+1)/2*img.size[1]) + (1-kh)*(ratiodiff*img.size[1]))))
            blurimg.paste(img, box=(round(kh*(ratiodiff-1)/2*img.size[0]), round((1-kh)*(ratiodiff-1)/2*img.size[1])))
            finalimg = blurimg
        finalimg.save('Processed/' + 'processed-' + img.filename)
        
if __name__ == '__main__':
    args = parse_arguments()
    main()
