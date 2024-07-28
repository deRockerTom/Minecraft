import numpy as np
import cv2
import math


class Fish:
    def should_fish(self, image_path: str, max_distance: int = 75) -> bool:
        """
        Check if the image contains a fish.
        """
        image = cv2.imread(image_path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Preprocess the image (convert to grayscale and apply edge detection)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)

        # Detect triangles in the image
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        triangles = []

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define the color range for detecting yellow triangles (adjust as needed)
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        # Create a mask for the yellow color
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Find contours in the masked image
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Filter and detect triangles
        triangles = []
        for contour in contours:
            epsilon = 0.05 * cv2.arcLength(
                contour, True
            )  # Adjusted epsilon for better approximation
            approx = cv2.approxPolyDP(contour, epsilon, True)
            if len(approx) == 3:
                triangles.append(approx)

        # Draw triangles on the image
        image_with_triangles = rgb.copy()
        cv2.drawContours(image_with_triangles, triangles, -1, (0, 255, 0), 2)

        # Check if triangles were detected
        if not triangles:
            print("No triangles detected.")
            return True

        # Detect the lowest pixel matching the yellow color in the image
        lowest_pixel = None
        for y in range(image.shape[0] - 1, 0, -1):
            for x in range(image.shape[1]):
                if mask[y, x] == 255:
                    lowest_pixel = (x, y)
                    break
            if lowest_pixel is not None:
                break

        # Draw the lowest pixel on the image
        if lowest_pixel is not None:
            cv2.circle(image_with_triangles, lowest_pixel, 5, (255, 0, 0), 25)

        cv2.imwrite("screenshots\\screen_debug.png", image_with_triangles)

        # Check if the lowest pixel is within the triangles
        min_distance = float("inf")
        if lowest_pixel is not None:
            x0, y0 = lowest_pixel
            for triangle in triangles:
                for point in triangle:
                    x1, y1 = point[0]
                    distance = math.sqrt((x1 - x0) ** 2)
                    if distance < min_distance:
                        min_distance = distance
        # print(f"Distance: {min_distance}")
        return min_distance < max_distance
