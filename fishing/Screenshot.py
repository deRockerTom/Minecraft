from PIL import ImageGrab


class Screenshot:
    def __init__(self, path: str, top: int, left: int, width: int, height: int):
        self.path = path
        self.top = top
        self.left = left
        self.width = width
        self.height = height

    def take(self):
        """
        Take a screenshot of the specified area of the screen.
        """
        screenshot = ImageGrab.grab(
            bbox=(self.left, self.top, self.left + self.width, self.top + self.height),
            all_screens=True,
        )
        screenshot.save(self.path)
        screenshot.close()
