    def draft(self, mode, size):
        """
        Configures the image file loader so it returns a version of the
        image that as closely as possible matches the given mode and
        size. For example, you can use this method to convert a color
        JPEG to grayscale while loading it.

        If any changes are made, returns a tuple with the chosen ``mode`` and
        ``box`` with coordinates of the original image within the altered one.

        Note that this method modifies the :py:class:`~PIL.Image.Image` object
        in place. If the image has already been loaded, this method has no
        effect.

        Note: This method is not implemented for most images. It is
        currently implemented only for JPEG and MPO images.

        :param mode: The requested mode.
        :param size: The requested size in pixels, as a 2-tuple:
           (width, height).
        """
        pass
