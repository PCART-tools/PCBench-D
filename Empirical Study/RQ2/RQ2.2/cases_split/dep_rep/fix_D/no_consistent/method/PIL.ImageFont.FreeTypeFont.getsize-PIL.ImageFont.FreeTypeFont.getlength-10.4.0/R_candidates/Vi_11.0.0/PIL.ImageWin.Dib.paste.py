    def paste(
        self, im: Image.Image, box: tuple[int, int, int, int] | None = None
    ) -> None:
        """
        Paste a PIL image into the bitmap image.

        :param im: A PIL image.  The size must match the target region.
                   If the mode does not match, the image is converted to the
                   mode of the bitmap image.
        :param box: A 4-tuple defining the left, upper, right, and
                    lower pixel coordinate.  See :ref:`coordinate-system`. If
                    None is given instead of a tuple, all of the image is
                    assumed.
        """
        im.load()
        if self.mode != im.mode:
            im = im.convert(self.mode)
        if box:
            self.image.paste(im.im, box)
        else:
            self.image.paste(im.im)
