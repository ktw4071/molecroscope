from time import time
import numpy as np
import cv2

def get_skew(mole_A, mole_B):

    """
    Given two images (Assuming they're of the same object), re-align the two pictures
    """

    return cv2.findHomography(np.float32(mole_A), np.float32(mole_B))

def enhance_lighting(image):

    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    height = image.shape[0]
    length = image.shape[1]

    def center_dist(x, y, mode = "Euclidean"):

        if mode == "Euclidean":

            # Return Euclidean distance of (x, y) to center

            return int(pow(pow(x - height / 2, 2) + pow(y - length / 2, 2), 0.5))

        elif mode == "Manhattan":

            # Return Manhattan distance of (x, y) to center

            return (abs(x - height / 2) + abs(y - length / 2)) / 4

    POWER = 1.3

    for y in xrange(height):
        for x in xrange(length):
            # 0 - Black
            # 255 - White
            image[y, x] = min(255, pow(max(0, image[y, x] - 60 + center_dist(y, x)), POWER))

    return image


def get_mole(image, points = 4):

    """
    Gets key points describing the mole
    """

    contours, _ = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mole = max(contours, key = lambda c: cv2.contourArea(c)).tolist()

    # Horizontal

    left = max(mole, key = lambda point: point[0][0])
    right = min(mole, key = lambda point: point[0][0])

    # Vertical

    top = max(mole, key = lambda point: point[0][1])
    bottom = min(mole, key = lambda point: point[0][1])

    return left, right, top, bottom

def process_image(image):

    # Resize Image
    width = image.shape[1]
    length = image.shape[0]
    scale = 0.1
    frame = cv2.resize(image, (int(width * scale), int(length * scale)))

    # Normalize Light Conditions
    FRAME = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    FRAME[:, :, 0] = cv2.equalizeHist(FRAME[:, :, 0])
    frame = cv2.cvtColor(FRAME, cv2.COLOR_YUV2BGR)

    # Isolate Mole
    frame = enhance_lighting(frame)

    # Convert to simpler Black or White Image
    frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, width >> 1 | 1, 2)

    return frame

def fix_alignment(img_A, img_B):
    # Grab Mole Contour

    mole_points_A = get_mole(img_A)

    mole_points_B = get_mole(img_B)

    perspective, status = get_skew(mole_points_A, mole_points_B)

    #img_A = draw_points(img_A, mole_points_A)
    #img_B = draw_points(img_B, mole_points_B)

    fixed_img = cv2.warpPerspective(img_A, perspective, (img_A.shape[1], img_A.shape[0]))

    return fixed_img

def get_difference(img_A, img_B, mode = "Overlap"):

    # Overlap
    if mode == "Overlap":
        length = img_A.shape[0]
        width  = img_A.shape[1]

        common_area = 0

        for x in xrange(length):
            for y in xrange(width):
                if img_A[x, y] == img_B[x, y] == 255:
                    common_area += 1

        return common_area



# ------------------------------------------------------------- #

def draw_points(img, points):
    points = np.int0(points)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for i in points:
        x, y = i.ravel()
        cv2.circle(img, (x, y), 3, (0, 20, 255), -1)
    return img

def save_image(image, filename):
    cv2.imwrite(filename, image)
    cv2.destroyAllWindows()

t0 = time()

FRAME_A = process_image(cv2.imread('mole1.jpg'))
FRAME_B = process_image(cv2.imread('mole.jpg'))

fixed_img = fix_alignment(FRAME_A, FRAME_B)

save_image(fixed_img, "output1.jpg")
save_image(FRAME_B, "output2.jpg")

print get_difference(fixed_img, FRAME_B)
print "TIME: %.5f" % (time() - t0)
