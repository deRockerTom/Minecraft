from PIL import Image
import imagehash
import os
import numpy as np


class Images:
    def find_nearest(self, reference: str, images: list[str]) -> str:
        """
        Find the image in the list that is the most similar to the reference image.
        """
        if images == []:
            raise ValueError("The list of images cannot be empty.")
        with Image.open(reference) as reference_image:
            hash = imagehash.average_hash(reference_image).hash
        closest_index = 0
        with Image.open(images[0]) as first_image:
            closest_distance = np.count_nonzero(
                imagehash.average_hash(first_image).hash != hash
            )

        for image in images:
            with Image.open(image) as image_data:
                distance = np.count_nonzero(
                    imagehash.average_hash(image_data).hash != hash
                )
                if distance < closest_distance:
                    closest_index = images.index(image)
                    closest_distance = distance
        return images[closest_index]

    def is_close(self, reference: str, image: str, epsilon: int = 10) -> bool:
        """
        Check if the image is similar to the reference image.
        """
        with Image.open(reference) as reference_image:
            hash = imagehash.average_hash(reference_image).hash
        with Image.open(image) as image_data:
            distance = np.count_nonzero(imagehash.average_hash(image_data).hash != hash)
        return distance < epsilon
