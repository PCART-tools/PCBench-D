    def set_data(self, A):
        """
        Set the image array.

        ACCEPTS: numpy/PIL Image A

        Note that this function does *not* update the normalization used.
        """
        # check if data is PIL Image without importing Image
        if hasattr(A, 'getpixel'):
            self._A = pil_to_array(A)
        else:
            self._A = cbook.safe_masked_invalid(A, copy=True)

        if (self._A.dtype != np.uint8 and
                not np.can_cast(self._A.dtype, float, "same_kind")):
            raise TypeError("Image data cannot be converted to float")

        if not (self._A.ndim == 2
                or self._A.ndim == 3 and self._A.shape[-1] in [3, 4]):
            raise TypeError("Invalid dimensions for image data")

        self._imcache = None
        self._rgbacache = None
        self.stale = True
