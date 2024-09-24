import cv2
import numpy as np
import time

#print(cv2.__version__)

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

blue_stickers_processed = np.zeros(image.shape, image.dtype)
green_stickers_processed = np.zeros(image.shape, image.dtype)
red_stickers_processed = np.zeros(image.shape, image.dtype)
yellow_stickers_processed = np.zeros(image.shape, image.dtype)

def export_dots():
    print("Exporting coloured dots from \'dotvotes_trimmed.jpg\', please wait")
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
    
    globals()["blue_stickers_image"] = blue_stickers_image
    globals()["green_stickers_image"] = green_stickers_image
    globals()["red_stickers_image"] = red_stickers_image
    globals()["yellow_stickers_image"] = yellow_stickers_image
    
    cv2.imwrite("blue_stickers_image.png", blue_stickers_image)
    cv2.imwrite("green_stickers_image.png", green_stickers_image)
    cv2.imwrite("red_stickers_image.png", red_stickers_image)
    cv2.imwrite("yellow_stickers_image.png", yellow_stickers_image)

def load_dots():
    globals()["blue_stickers_image"] = cv2.imread('blue_stickers_image.png')
    globals()["green_stickers_image"] = cv2.imread('green_stickers_image.png')
    globals()["red_stickers_image"] = cv2.imread('red_stickers_image.png')
    globals()["yellow_stickers_image"] = cv2.imread('yellow_stickers_image.png')

def load_dots_processed():
    globals()["blue_stickers_processed"] = cv2.imread('blue_stickers_processed.png')
    globals()["green_stickers_processed"] = cv2.imread('green_stickers_processed.png')
    globals()["red_stickers_processed"] = cv2.imread('red_stickers_processed.png')
    globals()["yellow_stickers_processed"] = cv2.imread('yellow_stickers_processed.png')

def morph_dots():
    #an ellipse shape for our operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
    
    #carry out our operations
    #morph_close is dilation followed by erosion
    #morph_open is erosion followed by dilation
    globals()["blue_stickers_processed"] = cv2.morphologyEx(blue_stickers_image, cv2.MORPH_OPEN, kernel)
    globals()["green_stickers_processed"] = cv2.morphologyEx(green_stickers_image, cv2.MORPH_OPEN, kernel)
    globals()["red_stickers_processed"] = cv2.morphologyEx(red_stickers_image, cv2.MORPH_OPEN, kernel)
    globals()["yellow_stickers_processed"] = cv2.morphologyEx(yellow_stickers_image, cv2.MORPH_OPEN, kernel)
    
    #export the finished images
    cv2.imwrite("blue_stickers_processed.png", globals()["blue_stickers_processed"])
    cv2.imwrite("green_stickers_processed.png", globals()["green_stickers_processed"])
    cv2.imwrite("red_stickers_processed.png", globals()["red_stickers_processed"])
    cv2.imwrite("yellow_stickers_processed.png", globals()["yellow_stickers_processed"])

def dilate_dots():
    #the dilation operation will fill in any random holes or gaps to make a "smooth" image    
    #an ellipse shape for our operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    
    #carry out our operations
    globals()["blue_stickers_processed"] = cv2.dilate(blue_stickers_image, kernel)
    globals()["green_stickers_processed"] = cv2.dilate(green_stickers_image, kernel)
    globals()["red_stickers_processed"] = cv2.dilate(red_stickers_image, kernel)
    globals()["yellow_stickers_processed"] = cv2.dilate(yellow_stickers_image, kernel)
    
    #export the finished images
    cv2.imwrite("blue_stickers_processed.png", blue_stickers_image)
    cv2.imwrite("green_stickers_processed.png", green_stickers_image)
    cv2.imwrite("red_stickers_processed.png", red_stickers_image)
    cv2.imwrite("yellow_stickers_processed.png", yellow_stickers_image)

def generate_contours(src_image, do_debug):
    #WIP
    threshold = 1
    src_gray = cv2.cvtColor(src_image, cv2.COLOR_BGR2GRAY)
    canny_output = cv2.Canny(src_gray, threshold, threshold * 2)
    contours,heirarchy = cv2.findContours(canny_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #loop over the array and remove any extraneous contours which are too small
    contours_trimmed = []
    area_threshold = 500
    testimg = np.zeros(image.shape, image.dtype)
    for i in range(0, len(contours)):
        #if it's too small to be a dot, it must be an artefact
        area = cv2.contourArea(contours[i])
        #print("area:" + str(area))
        if(do_debug):
            x,y,w,h = cv2.boundingRect(contours[i])
            cv2.rectangle(testimg,(x,y),(x+w,y+h),(0,200,0),1)
        if(area > area_threshold):
            contours_trimmed.append(contours[i])
    
    if(do_debug):
        print("contours_trimmed:" + str(len(contours_trimmed)))
        print("contours:" + str(len(contours)))
        
        #for i in range(1, len(contours_trimmed)):
            #print(cv2.contourArea(contours_trimmed[i]))
            #x,y,w,h = cv2.boundingRect(contours_trimmed[i])
            #cv2.rectangle(testimg,(x,y),(x+w,y+h),(0,200,0),1)
        cv2.imwrite("zzz_testimage.png", testimg)
    return contours_trimmed

def count_contours(src_image):
    return len(generate_contours(src_image, False))

def count_all_contours():
    num_blue = count_contours(globals()["blue_stickers_processed"])
    num_green = count_contours(globals()["green_stickers_processed"])
    num_red = count_contours(globals()["red_stickers_processed"])
    num_yellow = count_contours(globals()["yellow_stickers_processed"])
    print("Number of blue dots: " + str(num_blue))
    print("Number of green dots: " + str(num_green))
    print("Number of yellow dots: " + str(num_yellow))
    print("Number of red dots: " + str(num_red))



#carry out our operations... uncomment them as necessary
#export_dots()
#load_dots()
#dilate_dots()  #this one is unneeded
#morph_dots()
#load_dots_processed()
#generate_contours(globals()["red_stickers_processed"], True)
#count_all_contours()

