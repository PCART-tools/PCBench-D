    def entropy(
        self, mask: Image | None = None, extrema: tuple[float, float] | None = None
    ) -> float:
        """
        Calculates and returns the entropy for the image.

        A bilevel image (mode "1") is treated as a grayscale ("L")
        image by this method.

        If a mask is provided, the method employs the histogram for
        those parts of the image where the mask image is non-zero.
        The mask image must have the same size as the image, and be
        either a bi-level image (mode "1") or a grayscale image ("L").

        :param mask: An optional mask.
        :param extrema: An optional tuple of manually-specified extrema.
        :returns: A float value representing the image entropy
        """
        self.load()
        if mask:
            mask.load()
            return self.im.entropy((0, 0), mask.im)
        if self.mode in ("I", "F"):
            return self.im.entropy(
                extrema if extrema is not None else self.getextrema()
            )
        return self.im.entropy()
