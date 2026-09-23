    def paste(self, im, box=None, mask=None) -> None:
        """
        Pastes another image into this image. The box argument is either
        a 2-tuple giving the upper left corner, a 4-tuple defining the
        left, upper, right, and lower pixel coordinate, or None (same as
        (0, 0)). See :ref:`coordinate-system`. If a 4-tuple is given, the size
        of the pasted image must match the size of the region.

        If the modes don't match, the pasted image is converted to the mode of
        this image (see the :py:meth:`~PIL.Image.Image.convert` method for
        details).

        Instead of an image, the source can be a integer or tuple
        containing pixel values.  The method then fills the region
        with the given color.  When creating RGB images, you can
        also use color strings as supported by the ImageColor module.

        If a mask is given, this method updates only the regions
        indicated by the mask. You can use either "1", "L", "LA", "RGBA"
        or "RGBa" images (if present, the alpha band is used as mask).
        Where the mask is 255, the given image is copied as is.  Where
        the mask is 0, the current value is preserved.  Intermediate
        values will mix the two images together, including their alpha
        channels if they have them.

        See :py:meth:`~PIL.Image.Image.alpha_composite` if you want to
        combine images with respect to their alpha channels.

        :param im: Source image or pixel value (integer or tuple).
        :param box: An optional 4-tuple giving the region to paste into.
           If a 2-tuple is used instead, it's treated as the upper left
           corner.  If omitted or None, the source is pasted into the
           upper left corner.

           If an image is given as the second argument and there is no
           third, the box defaults to (0, 0), and the second argument
           is interpreted as a mask image.
        :param mask: An optional mask image.
        """

        if isImageType(box) and mask is None:
            # abbreviated paste(im, mask) syntax
            mask = box
            box = None

        if box is None:
            box = (0, 0)

        if len(box) == 2:
            # upper left corner given; get size from image or mask
            if isImageType(im):
                size = im.size
            elif isImageType(mask):
                size = mask.size
            else:
                # FIXME: use self.size here?
                msg = "cannot determine region size; use 4-item box"
                raise ValueError(msg)
            box += (box[0] + size[0], box[1] + size[1])

        if isinstance(im, str):
            from . import ImageColor

            im = ImageColor.getcolor(im, self.mode)

        elif isImageType(im):
            im.load()
            if self.mode != im.mode:
                if self.mode != "RGB" or im.mode not in ("LA", "RGBA", "RGBa"):
                    # should use an adapter for this!
                    im = im.convert(self.mode)
            im = im.im

        self._ensure_mutable()

        if mask:
            mask.load()
            self.im.paste(im, box, mask.im)
        else:
            self.im.paste(im, box)
