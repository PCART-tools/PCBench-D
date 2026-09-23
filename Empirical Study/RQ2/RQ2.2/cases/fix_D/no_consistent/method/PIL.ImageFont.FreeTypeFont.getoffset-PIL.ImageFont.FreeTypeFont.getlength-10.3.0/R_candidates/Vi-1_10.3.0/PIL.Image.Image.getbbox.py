    def getbbox(self, *, alpha_only: bool = True) -> tuple[int, int, int, int]:
        """
        Calculates the bounding box of the non-zero regions in the
        image.

        :param alpha_only: Optional flag, defaulting to ``True``.
           If ``True`` and the image has an alpha channel, trim transparent pixels.
           Otherwise, trim pixels when all channels are zero.
           Keyword-only argument.
        :returns: The bounding box is returned as a 4-tuple defining the
           left, upper, right, and lower pixel coordinate. See
           :ref:`coordinate-system`. If the image is completely empty, this
           method returns None.

        """

        self.load()
        return self.im.getbbox(alpha_only)
