import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")
from libs.image_enhancement import *
import tifffile as tiff
import os

# The camera opens and an ellipse is drawn on the screen. Inside the ellipse
# there is the image the area sees and the outside is all white. The fingerprint
# area is placed inside the ellipse to capture the necessary and well displayed area.
# Then the photograph is captured, processed and saved in a directory with the appropriate
# name(the users name) along with other users photos. The snippet of code that will
# draw the ellipse looks something like the code bellow.

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

''' Now for the registration '''


def register(username):
    # load_path should be a directory that will store the image captured during registration,
    # then process it below, save the processed image in the designated directory and then DELETE the image from
    # the load_path directory to keep it empty for the next registration.

    # Image is already in the directory and only thing left is the processing

    load_path = 'load_directory/' + username + '.jpg'  # Change path (and extension if needed)!!!
    image = cv.imread(load_path)  # Load image the user captured

    enhancer = ProcessEnhance()  # enhancer object is created that will enhance the image to the desired format.

    enhanced_image = enhancer.process(image, clipLimit=4, tileGridSize=(20, 20)).astype('uint8')

    # Now I want to save the enhanced image to the directory where all the others are saved with the name of the user.
    save_path = 'save_directory/' + username + '.tif'
    tiff.imwrite(save_path, enhanced_image)

    # Now delete the image loaded while checking if it exists
    if os.path.exists(load_path):
        # Delete the image
        os.remove(load_path)
    else:
        print("Image not found!")


""" Get the username from where it was stored when the user entered it in the frontend (with open(), GET etc.). """

username = 'name'  # use above method
register(username)
