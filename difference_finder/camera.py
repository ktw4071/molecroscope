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

def normalize_lighting(image):

    if len(image.shape) < 3:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)

    image[:, :, 0] = cv2.equalizeHist(image[:, :, 0])

    return cv2.cvtColor(image, cv2.COLOR_YUV2BGR)

def get_blobs(image):

    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        # draw the contour and show it
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    return image

#cap = cv2.VideoCapture(0)
#print(cap.isOpened()) # False

# Capture frame-by-frame
#ret, frame = cap.read()
while 1:
    frame = cv2.imread('mole.jpg')
    #frame1 = cv2.imread('mole1.jpg')

    # Our operations on the frame come here
    kernel = np.array([
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1]])

    # Resize Image
    width = frame.shape[1]
    length = frame.shape[0]
    scale = 0.1
    frame = cv2.resize(frame, (int(width * scale), int(length * scale)))

    # Contrast Filter
    contrast = 70
    f = 131*(contrast + 127)/(127*(131-contrast))
    alpha_c = f
    gamma_c = 127*(1-f)

    frame = cv2.addWeighted(frame, alpha_c, frame, 0, gamma_c)

    # Img Operations

    # Method 1
    #frame = cv2.filter2D(frame, -1, kernel)

    # Method 2
    #frame = cv2.addWeighted(frame, 4, cv2.blur(frame, (30, 30)), -4, 128)


    # Display the resulting frame

    #frame = align_images(frame, frame1)
    array_alpha = np.array([1.5])
    array_beta = np.array([25.0])

    # add a beta value to every pixel
    #frame = cv2.add(frame, array_beta, frame)

    # multiply every pixel value by alpha
    frame = cv2.multiply(cv2.multiply(frame, array_alpha, frame), array_alpha, frame)

    #frame = align_images(frame, frame1)

    # Light Normalize
    #frame = normalize_lighting(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, frame.shape[0] | 1, 1)
    ret, frame = cv2.threshold(frame, 150, 255, cv2.THRESH_BINARY)

    #ret, frame = cv2.threshold(frame, 255, 255, cv2.THRESH_TRUNC)
    #frame = normalize_lighting(frame)
    cv2.imshow('Sharpened Version', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
#cap.release()
cv2.destroyAllWindows()