# referenced tutorial: https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/
# import packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import crop
import re

whitelist = "-c tessedit_char_whitelist=#abcdefghijklmnopqrstuvwxyz123456789"
psm    = "--psm 11"
config = psm + " " + whitelist

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str,
	help="type of preprocessing to be done")
ap.add_argument("-os", "--system", type=str,
	help="specify OS if on windows")
args = vars(ap.parse_args())

if args["system"] == "win":
	pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# load the example image 
image = cv2.imread(args["image"])
# percent of original image size
c = None
limit = 500
# check if rescale necessary: h/w = h'/w', w/h = w'/h'
if image.shape[0] > limit:
	c = float(image.shape[0]) # original height
	height = limit
	width  = image.shape[1]/c * height
elif image.shape[1] > limit:
	c = float(image.shape[1]) # original width
	width  = limit
	height = image.shape[0]/c * width
# must rescale
if c:
	new_dim = (int(width), int(height))
	image = cv2.resize(image, new_dim, interpolation=cv2.INTER_AREA)

# grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# check to see if we should apply thresholding to preprocess the
# image
if args["preprocess"] == "thresh":
	gray = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
 
# make a check to see if median blurring should be done to remove
# noise
elif args["preprocess"] == "blur":
	gray = cv2.medianBlur(gray, 3)

# contrast
elif args["preprocess"] == "contrast":
	gray = 2*gray
 
# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
ospid = os.getpid()
filename = "cache/{}.png".format(ospid)
cv2.imwrite(filename, gray)
processed_img = Image.open(filename)

# find interest points
boxes = pytesseract.image_to_boxes(processed_img, config=config)
gray = crop.bound_by_symbol(processed_img, boxes, symbol='#', show_boxes=True)

# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
text = pytesseract.image_to_string(gray, config=config)
os.remove(filename)

# cropped_data = pytesseract.image_to_data(gray, config=config, output_type=pytesseract.Output.DICT)
# crop.detect_computing_ids(gray, cropped_data)

# filter out invalid ids
id_regex = r'([a-z]{2}|[a-z]{3})[1-9][a-z]{2}'
suffix   = "@virginia.edu"
ids = [s+suffix for s in text.split('\n') 
	   if re.match(id_regex,s) and (5 <= len(s) <= 6)]
print(ids)
 
# show the output images
cv2.imshow("Output", gray)
cv2.waitKey(0)