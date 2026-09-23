    def get_width_height(self):
        """
        Return the figure width and height in points or pixels
        (depending on the backend), truncated to integers.
        """
        return int(self.figure.bbox.width), int(self.figure.bbox.height)
