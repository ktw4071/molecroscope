from time import time
import numpy as np
import cv2

def enhance_lighting(image):

    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    height = image.shape[0]
    length = image.shape[1]

    cnt_height = height >> 1
    cnt_length = length >> 1

    def center_dist(x, y):

        # Return Euclidean distance of point to the center

        return int(pow(pow(x - cnt_height, 2) + pow(y - cnt_length, 2), 0.5))

    POWER = 1.3

    for y in xrange(height):
        for x in xrange(length):
            # 0 - Black
            # 255 - White
            image[y, x] = min(255, int(pow(max(0, image[y, x] - 60 + center_dist(y, x)), POWER)))

    return image


def get_mole(img1, img2, points = 4):

    """
    Gets key points describing the mole
    """

    detector = cv2.FeatureDetector_create("SURF")
    descriptor = cv2.DescriptorExtractor_create("BRIEF")
    matcher = cv2.DescriptorMatcher_create("BruteForce-Hamming")

    # detect keypoints
    kp1 = detector.detect(img1)
    kp2 = detector.detect(img2)

    # descriptors
    k1, d1 = descriptor.compute(img1, kp1)
    k2, d2 = descriptor.compute(img2, kp2)

    # match the keypoints
    matches = matcher.match(d1, d2)

    matches.sort(key = lambda i: i.distance)

    key_a = []
    key_b = []

    for mat in matches[:points if points < 20 else len(matches)]:
        key_a.append(kp1[mat.queryIdx].pt)
        key_b.append(kp2[mat.trainIdx].pt)

    return key_a, key_b

def process_image(image):

    # Resize Image

    scale = 10
    frame = cv2.resize(image, (image.shape[1] / scale, image.shape[0] / scale))

    width = frame.shape[1]
    length = frame.shape[0]

    # Normalize Light Conditions
    FRAME = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    FRAME[:, :, 0] = cv2.equalizeHist(FRAME[:, :, 0])
    frame = cv2.cvtColor(FRAME, cv2.COLOR_YUV2BGR)

    # Isolate Mole
    frame = enhance_lighting(frame)


    # Convert to simpler Black or White Image
    frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, width >> 1 | 1, 2)

    # Fill in all the visual artifacts (Smaller spots)

    contours, _ = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mole = max(contours, key = lambda c: cv2.contourArea(c))

    for x in xrange(length):
        for y in xrange(width):
            if frame[x, y] == 255:
                if cv2.pointPolygonTest(mole, (y, x), False) == -1:
                    frame[x, y] = 0

    return frame

def fix_alignment(img, key_src, key_dest):

    # Correct image with detected keypoints

    perspective, status = cv2.findHomography(np.float32(key_src), np.float32(key_dest))

    return cv2.warpPerspective(img, perspective, (img.shape[1], img.shape[0]))

def get_difference(img_A, img_B):

    mode = "K"

    if mode == "O":

        length = img_A.shape[0]
        width  = img_A.shape[1]

        common_area = 0
        total_area  = 0

        for x in xrange(length):
            for y in xrange(width):
                if img_B[x, y] == 255:
                    total_area += 1
                    if img_A[x, y] == 255:
                        common_area += 1

        return 1 - float(common_area) / total_area

    elif mode == "K":

        key_a, key_b = get_mole(img_A, img_B)

        total_differences = 0

        for (x1, y1), (x2, y2) in zip(key_a, key_b):
            total_differences += pow(pow(x1 - x2, 2) + pow(y1 - y2, 2), 0.5)

        return min(100, total_differences / len(key_a))

# ------------------------------------------------------------- #

def draw_points(img, points = None):

    if not points:
        points = get_mole(img)

    points = np.int0(points)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    side_length = 4
    for i in points:
        x, y = i.ravel()
        cv2.rectangle(img, (x - side_length, y - side_length), (x + side_length, y + side_length), (0, 20, 255), 2)
    return img

def save_image(image, filename):
    cv2.imwrite(filename, image)
    cv2.destroyAllWindows()


def main():
    t0 = time()

    FRAME_A = process_image(cv2.imread('mole1.jpg'))

    FRAME_B = process_image(cv2.imread('mole.jpg'))

    key_a, key_b = get_mole(FRAME_A, FRAME_B, 11)

    fixed_img = fix_alignment(FRAME_A, key_a, key_b)

    save_image(fixed_img, "output1.jpg")
    save_image(FRAME_B, "output2.jpg")

    #cv2.imshow('tet', fixed_img)

    #Set waitKey
    #cv2.waitKey()


    #cv2.imshow('tet50', FRAME_B)

    #Set waitKey
    #cv2.waitKey()

    print("TIME: %.5f" % (time() - t0))

    return get_difference(fixed_img, FRAME_B)
