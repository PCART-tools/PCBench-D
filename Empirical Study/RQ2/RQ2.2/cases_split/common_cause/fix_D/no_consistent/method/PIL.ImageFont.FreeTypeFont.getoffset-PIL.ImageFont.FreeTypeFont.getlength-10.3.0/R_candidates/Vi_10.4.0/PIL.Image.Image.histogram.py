    def histogram(self, mask: Image | None = None, extrema=None) -> list[int]:
        """
        Returns a histogram for the image. The histogram is returned as a
        list of pixel counts, one for each pixel value in the source
        image. Counts are grouped into 256 bins for each band, even if
        the image has more than 8 bits per band. If the image has more
        than one band, the histograms for all bands are concatenated (for
        example, the histogram for an "RGB" image contains 768 values).

        A bilevel image (mode "1") is treated as a grayscale ("L") image
        by this method.

        If a mask is provided, the method returns a histogram for those
        parts of the image where the mask image is non-zero. The mask
        image must have the same size as the image, and be either a
        bi-level image (mode "1") or a grayscale image ("L").

        :param mask: An optional mask.
        :param extrema: An optional tuple of manually-specified extrema.
        :returns: A list containing pixel counts.
        """
        self.load()
        if mask:
            mask.load()
            return self.im.histogram((0, 0), mask.im)
        if self.mode in ("I", "F"):
            if extrema is None:
                extrema = self.getextrema()
            return self.im.histogram(extrema)
        return self.im.histogram()
