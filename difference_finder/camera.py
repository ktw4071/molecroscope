import numpy as np
import cv2

def align_images(img1, img2):
    """
    Given two images (Assuming they're of the same object), re-align the two pictures
    """

    # Convert pictures to grayscale
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Get contour of the mole

    POINTS = 5 # Number of points to find
    QUALITY = 0.000001 # Threshold of key point quality
    DISTANCE = 1 # Distance between all good points (Not really important)

    contour_A = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #contour_B = cv2.goodFeaturesToTrack(gray_img2, POINTS, QUALITY, DISTANCE)

    key_points_A = np.int0(key_points_A)

    for i in key_points_A:
        x,y = i.ravel()
        cv2.circle(gray_img1, (x, y), 5, (0, 20, 200), 1)

    return gray_img1

def enhance_lighting(image):

    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    height = image.shape[0]
    length = image.shape[1]

    def center_dist(x, y, mode = "Manhattan"):

        if mode == "Euclid":

            # Return Euclidean distance of (x, y) to center

            return int(pow(pow(x - height / 2, 2) + pow(y - length / 2, 2), 0.5)) / 80

        elif mode == "Manhattan":

            # Return Manhattan distance of (x, y) to center

            return (abs(x - height / 2) + abs(y - length / 2)) / 2

    POWER = 1.3

    for y in xrange(height):
        for x in xrange(length):
            # 0 - Black
            # 255 - White
            image[y, x] = min(255, pow(max(0, image[y, x] - 90 + center_dist(y, x)), POWER))

    return image

# Capture frame-by-frame
#ret, frame = cap.read()

FRAME = cv2.imread('mole.jpg')

# Resize Image

width = FRAME.shape[1]
length = FRAME.shape[0]
scale = 0.1
frame = cv2.resize(FRAME, (int(width * scale), int(length * scale)))

frame = enhance_lighting(frame)

while 1:

    cv2.imshow('Sharpened Version', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
#cap.release()
cv2.destroyAllWindows()
