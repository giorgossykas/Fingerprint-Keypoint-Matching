import os
import cv2 as cv

from libs.basics import *
from libs.edges import *
from libs.enhancing import *
from libs.image_enhancement import *
from libs.matching import *
from libs.minutiae import *
from libs.processing import *
import sys
import tifffile as tiff
from main import *

# After a user has registered he can then authenticate himself by taking a picture of his fingerprint.
# His fingerprint area will be placed in the same elliptic shape as the registration method and again
# be processed. Then the key-points of that picture will be compared to the key-points of all the other
# stored images from the users and if there are more than the threshold matched key-points the user will be recognized.
# Again the same snippet of code for the camera opening and capturing the image will be used. This image will once again
# be TEMPORARILY saved in the load_directory or load_path to be tested against the saved images inside the save_path or save_directory.

"""
import cv2
import numpy as np

# Create a VideoCapture object to access the webcam (by default, it opens the first camera)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Calculate the center of the frame
    center_x, center_y = width // 2, height // 2

    # Define the parameters of the ellipse
    axes = (200, 100)  # Major and minor axes of the ellipse, modify them depending on the camera resolution.
    angle = 0  # Rotation angle (in degrees). Maybe you need to rotate 90 degrees depending on finger placement.
    color = (255, 255, 255)  # BGR color format (white)
    thickness = -1  # Fills the ellipse

    # Create a blank image with the same dimensions as the frame
    blank_image = np.zeros_like(frame)

    # Draw a filled ellipse on the blank image
    cv2.ellipse(blank_image, (center_x, center_y), axes, angle, 0, 360, color, thickness)
    blank_image = 255 - blank_image # Makes outside white and inside black

    # Combine the blank image with the webcam frame to make the area outside the ellipse white
    result = cv2.addWeighted(frame, 1, blank_image, 1, 0)

    # Show the result with the ellipse and white background
    cv.namedWindow('result', cv.WINDOW_NORMAL)
    cv.resizeWindow('result', 600, 600) # Again these values will be adjusted depending on your screen size and resolution
    cv2.imshow('Webcam with Ellipse', result)


    # Add code that lets the user capture the image here, and save it with the appropriate name.


    # Exit the loop when the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
"""


''' Now for the authentication '''

def authenticate():

    # load_path should be a directory that will store the image captured during authenticate,
    # then process it below, save the processed image in the designated directory and then DELETE the image from
    # the load_path directory to keep it empty for the next authentication.

    # Image is already in the directory and only thing left is the processing

    # Specify the directory containing the image and the directory where all images of registered users are saved.
    load_path = 'C:/Users/giorgossykas/Desktop'  # 'load_directory'
    save_path = 'C:/Users/giorgossykas/Desktop/Python scripts/Fingerprint recognition notebook/data/tif_new/' # 'load_directory'

    # List all files in the directory (should contain only one image)
    files = os.listdir(load_path)

    # Filter for image files (you can modify this condition based on your image file types)
    image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tif'))]

    if len(image_files) == 1:
        # Load the only image in the directory
        image_path = os.path.join(load_path, image_files[0])
        user_image = cv.imread(image_path)  # This is the first form of the image. Later I will change by loading it with load_image from fm object

        if user_image is not None:
            # Now I have the image, and it needs to be processed
            enhancer = ProcessEnhance()  # enhancer object is created that will enhance the image to the desired format.

            enhanced_image = enhancer.process(user_image, clipLimit=4, tileGridSize=(20, 20)).astype('uint8')

            # Now I have to compare the image across alla other saved images
            # First create the object of the FingerMatch class.
            fm = FingerMatch('orb')  # 'orb' is one of three ways to find key-points, usually most effective
            fm.loadData(save_path)   # Now the object has all the saved(already processed) images from registered users.
            fm.trainData()           # Training will be skipped in 'orb' mode. I will suppress the output that says it was skipped.
            #user_image = load_image(image_path, True)
            print(user_image.shape)
            print(fm.images[0].img_id)
            print(type(user_image))
            scores = fm.matchFingerprint(enhanced_image, verbose=False)


            # Now I will find all the matches and keep only the good key-points
            totals = []
            for j in range(len(scores)):

                match_mask = [[0, 0] for i in range(len(scores[j]))]

                for i, (m, n) in enumerate(scores[j]):
                    if m.distance < 0.7 * n.distance:
                        match_mask[i] = [1, 0]
                totals.append(match_mask)
            condition = lambda x: x == [1, 0]
            counts = []
            for i in range(len(scores)):
                counts.append(len([x for x in totals[i] if condition(x)]))

            # Variable "counts" has number of matches between the captures image and all other images.
            # For example if I have 15 registered users, "counts" will be a list of integers of good matches for
            # each registered user. If a count is larger that the threshold I will get the name of the image(username)
            # and authenticate him. If more than one matches are found I will take the picture again. Same if no
            # matches are found.
            threshold = 11
            index = [index for index, element in enumerate(counts) if element >= threshold]

            if len(index) == 0:
                print("No match found! Please take another picture.")
                return
            elif len(index) == 1:
                username = fm.images[index[0]].img_id
                print(f"Match found: User is {username}")
                return
            else:
                print("More than one users found.\nPlease take another picture.")
                return

        else:
            print("Failed to load the image!")

    else:
        print("There is not exactly one image in the directory or no image files were found!")




authenticate()