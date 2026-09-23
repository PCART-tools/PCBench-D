    def alpha_composite(self, im, dest=(0, 0), source=(0, 0)):
        """'In-place' analog of Image.alpha_composite. Composites an image
        onto this image.

        :param im: image to composite over this one
        :param dest: Optional 2 tuple (left, top) specifying the upper
          left corner in this (destination) image.
        :param source: Optional 2 (left, top) tuple for the upper left
          corner in the overlay source image, or 4 tuple (left, top, right,
          bottom) for the bounds of the source rectangle

        Performance Note: Not currently implemented in-place in the core layer.
        """

        if not isinstance(source, (list, tuple)):
            msg = "Source must be a tuple"
            raise ValueError(msg)
        if not isinstance(dest, (list, tuple)):
            msg = "Destination must be a tuple"
            raise ValueError(msg)
        if len(source) not in (2, 4):
            msg = "Source must be a 2 or 4-tuple"
            raise ValueError(msg)
        if not len(dest) == 2:
            msg = "Destination must be a 2-tuple"
            raise ValueError(msg)
        if min(source) < 0:
            msg = "Source must be non-negative"
            raise ValueError(msg)

        if len(source) == 2:
            source = source + im.size

        # over image, crop if it's not the whole thing.
        if source == (0, 0) + im.size:
            overlay = im
        else:
            overlay = im.crop(source)

        # target for the paste
        box = dest + (dest[0] + overlay.width, dest[1] + overlay.height)

        # destination image. don't copy if we're using the whole image.
        if box == (0, 0) + self.size:
            background = self
        else:
            background = self.crop(box)

        result = alpha_composite(background, overlay)
        self.paste(result, box)
