    def draw(
        self,
        handle: int | HDC | HWND,
        dst: tuple[int, int, int, int],
        src: tuple[int, int, int, int] | None = None,
    ) -> None:
        """
        Same as expose, but allows you to specify where to draw the image, and
        what part of it to draw.

        The destination and source areas are given as 4-tuple rectangles. If
        the source is omitted, the entire image is copied. If the source and
        the destination have different sizes, the image is resized as
        necessary.
        """
        if src is None:
            src = (0, 0) + self.size
        handle_int = int(handle)
        if isinstance(handle, HWND):
            dc = self.image.getdc(handle_int)
            try:
                self.image.draw(dc, dst, src)
            finally:
                self.image.releasedc(handle_int, dc)
        else:
            self.image.draw(handle_int, dst, src)
