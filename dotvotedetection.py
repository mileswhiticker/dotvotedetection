import cv2
import numpy as np
import time

#blue dot sticker: (1,62,168) RGB
#green dot sticker: (2,58,33) RGB
#red dot sticker: (140,34,38) RGB
#yellow dot sticker: (161,149,1) RGB

# Load image, grayscale, Otsu's threshold
image = cv2.imread('dotvotes_trimmed.jpg')
height, width, n_channels = image.shape

#a helper class to store our colour information
#opencv probably has a class for this already but i wanted specific and light functionality
class rgb:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    def close_enough(self, rgb_other):
        #threshold of 25 seems to be "close enough" to get the dots because they are fairly contiguous colours
        threshold = 25
        check_r = abs(self.r - rgb_other.r)
        check_g = abs(self.g - rgb_other.g)
        check_b = abs(self.b - rgb_other.b)
        if(check_r > threshold):
            return False
        if(check_g > threshold):
            return False
        if(check_b > threshold):
            return False
        return True

#i manually extracted these from the image
blue_sticker = rgb(1,62,168)
green_sticker = rgb(2,58,33)
red_sticker = rgb(140,34,38)
yellow_sticker = rgb(161,149,1)

blue_stickers_image = np.zeros(image.shape, image.dtype)
green_stickers_image = np.zeros(image.shape, image.dtype)
red_stickers_image = np.zeros(image.shape, image.dtype)
yellow_stickers_image = np.zeros(image.shape, image.dtype)

def export_dots():

    #write over these with the dot stickers we find
    #this function should take about 1-2 minutes so i added timing to help track it
    global blue_stickers_image
    global green_stickers_image
    global red_stickers_image
    global yellow_stickers_image
    
    #some helper variables for the loop
    maxval = height * width
    curval = 0
    num_intervals = 100
    progress_interval = round(maxval / num_intervals)
    cur_interval = 0

    #loop over all pixels in the image
    start_time = time.time()
    last_time = time.time()
    for j in range(1, height - 1):
        for i in range(1, width - 1):
            
            #some debugging and helpers
            curval += 1
            do_debug = False
            if(curval % progress_interval == 0):
                cur_interval += 1
                progress = round(100*curval/maxval)
                do_debug = True
                cur_time = time.time()
                time_taken = cur_time - last_time
                est_time_left = (num_intervals - cur_interval) * time_taken
                last_time = cur_time
                
                print("Progress: " + str(progress) + "% estimated time remaining: " + str(round(est_time_left)) + " seconds")

            #grab the colour of this pixel
            #remember that open_cv uses bgr format by default
            _blue = image[j,i,0]
            _green = image[j,i,1]
            _red = image[j,i,2]
            cur_pixel_colour = rgb(_red, _green, _blue)
            
            #try and figure out which output image to put it in
            if(blue_sticker.close_enough(cur_pixel_colour)):
                blue_stickers_image[j,i,0] = blue_sticker.b
                blue_stickers_image[j,i,1] = blue_sticker.g
                blue_stickers_image[j,i,2] = blue_sticker.r
            elif(green_sticker.close_enough(cur_pixel_colour)):
                green_stickers_image[j,i,0] = green_sticker.b
                green_stickers_image[j,i,1] = green_sticker.g
                green_stickers_image[j,i,2] = green_sticker.r
            elif(red_sticker.close_enough(cur_pixel_colour)):
                red_stickers_image[j,i,0] = red_sticker.b
                red_stickers_image[j,i,1] = red_sticker.g
                red_stickers_image[j,i,2] = red_sticker.r
            elif(yellow_sticker.close_enough(cur_pixel_colour)):
                yellow_stickers_image[j,i,0] = yellow_sticker.b
                yellow_stickers_image[j,i,1] = yellow_sticker.g
                yellow_stickers_image[j,i,2] = yellow_sticker.r
            
            if(curval > maxval):
                break
        if(curval > maxval):
            break

    time_taken = last_time - start_time
    print("Completed. Time taken: " + str(round(time_taken)) + " seconds")

    cv2.imwrite("blue_stickers_image.jpg", blue_stickers_image)
    cv2.imwrite("green_stickers_image.jpg", green_stickers_image)
    cv2.imwrite("red_stickers_image.jpg", red_stickers_image)
    cv2.imwrite("yellow_stickers_image.jpg", yellow_stickers_image)

def load_dots():
    blue_stickers_image = cv2.imread('blue_stickers_image.jpg')
    green_stickers_image = cv2.imread('green_stickers_image.jpg')
    red_stickers_image = cv2.imread('red_stickers_image.jpg')
    yellow_stickers_image = cv2.imread('yellow_stickers_image.jpg')

def dilate_dots():
    global blue_stickers_image
    global green_stickers_image
    global red_stickers_image
    global yellow_stickers_image

    #the dilation operation will fill in any random holes or gaps to make a "smooth" image


#carry out our operations
#export_dots()  #only need to do this once
load_dots()
dilate_dots()

#cv2.imshow('blue_stickers_image', blue_stickers_image)
#cv2.imshow('green_stickers_image', green_stickers_image)
#cv2.imshow('red_stickers_image', red_stickers_image)
#cv2.imshow('yellow_stickers_image', yellow_stickers_image)
cv2.waitKey()







###EXAMPLE CODE###

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Filter out large non-connecting objects
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    if area < 500:
        cv2.drawContours(thresh,[c],0,0,-1)

# Morph open using elliptical shaped kernel
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)

# Find circles 
cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    if area > 20 and area < 50:
        ((x, y), r) = cv2.minEnclosingCircle(c)
        cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)

#cv2.imshow('thresh', thresh)
#cv2.imshow('opening', opening)
#cv2.imshow('Dot votes image', image)
#cv2.waitKey()
