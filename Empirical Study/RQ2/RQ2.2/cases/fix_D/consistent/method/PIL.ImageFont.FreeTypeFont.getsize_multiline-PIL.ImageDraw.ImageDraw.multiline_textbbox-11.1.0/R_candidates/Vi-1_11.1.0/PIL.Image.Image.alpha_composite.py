    def alpha_composite(
        self, im: Image, dest: Sequence[int] = (0, 0), source: Sequence[int] = (0, 0)
    ) -> None:
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
            msg = "Source must be a list or tuple"
            raise ValueError(msg)
        if not isinstance(dest, (list, tuple)):
            msg = "Destination must be a list or tuple"
            raise ValueError(msg)

        if len(source) == 4:
            overlay_crop_box = tuple(source)
        elif len(source) == 2:
            overlay_crop_box = tuple(source) + im.size
        else:
            msg = "Source must be a sequence of length 2 or 4"
            raise ValueError(msg)

        if not len(dest) == 2:
            msg = "Destination must be a sequence of length 2"
            raise ValueError(msg)
        if min(source) < 0:
            msg = "Source must be non-negative"
            raise ValueError(msg)

        # over image, crop if it's not the whole image.
        if overlay_crop_box == (0, 0) + im.size:
            overlay = im
        else:
            overlay = im.crop(overlay_crop_box)

        # target for the paste
        box = tuple(dest) + (dest[0] + overlay.width, dest[1] + overlay.height)

        # destination image. don't copy if we're using the whole image.
        if box == (0, 0) + self.size:
            background = self
        else:
            background = self.crop(box)

        result = alpha_composite(background, overlay)
        self.paste(result, box)
