import cv2
import numpy as np
from picamera2 import Picamera2, Preview
from libcamera import Transform, controls
import time
import sys
import time

HEIGHT = 400
WIDTH  = 400

camera = Picamera2()
Configuration = camera.create_preview_configuration(main={"format": "RGB888", "size": (WIDTH, HEIGHT)}, transform = Transform(vflip=0, hflip=0))
camera.configure(Configuration)
camera.start()
camera.set_controls({"AfMode":controls.AfModeEnum.Continuous})
cv2.startWindowThread()

try:
    while True:
        start = time.time()

        image = camera.capture_array()


        tl = (50, 250)
        bl = (0, HEIGHT)
        tr = (350, 250)
        br = (WIDTH, HEIGHT)

        cv2.circle(image, tl, 3, (255, 0, 0), -1)
        cv2.circle(image, tr, 3, (255, 0, 0), -1)
        cv2.circle(image, bl, 3, (255, 0, 0), -1)
        cv2.circle(image, br, 3, (255, 0, 0), -1)

        corners = np.float32([tl, bl, tr, br])
        adjustedCorners = np.float32([[0, 0], [0, 400], [400, 0], [400, 400]])

        matrix = cv2.getPerspectiveTransform(corners, adjustedCorners)
        transformedImage = cv2.warpPerspective(image, matrix, (400, 400))

        cv2.imshow("image", image)
        cv2.imshow("transformed", transformedImage)

        print(f"{1 / (time.time() - start):.2f}")

except KeyboardInterrupt:
    print("Exiting Gracefully")

finally:
    camera.close()