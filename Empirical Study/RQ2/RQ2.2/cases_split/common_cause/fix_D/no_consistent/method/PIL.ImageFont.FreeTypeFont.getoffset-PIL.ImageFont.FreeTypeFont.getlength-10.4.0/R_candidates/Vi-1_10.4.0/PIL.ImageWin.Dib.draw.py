    def draw(self, handle, dst, src=None):
        """
        Same as expose, but allows you to specify where to draw the image, and
        what part of it to draw.

        The destination and source areas are given as 4-tuple rectangles. If
        the source is omitted, the entire image is copied. If the source and
        the destination have different sizes, the image is resized as
        necessary.
        """
        if not src:
            src = (0, 0) + self.size
        if isinstance(handle, HWND):
            dc = self.image.getdc(handle)
            try:
                result = self.image.draw(dc, dst, src)
            finally:
                self.image.releasedc(handle, dc)
        else:
            result = self.image.draw(handle, dst, src)
        return result
