    def set_data(self, A):
        """
        Set the image array.

        Note that this function does *not* update the normalization used.

        Parameters
        ----------
        A : array-like or `PIL.Image.Image`
        """
        if isinstance(A, PIL.Image.Image):
            A = pil_to_array(A)  # Needed e.g. to apply png palette.
        self._A = cbook.safe_masked_invalid(A, copy=True)

        if (self._A.dtype != np.uint8 and
                not np.can_cast(self._A.dtype, float, "same_kind")):
            raise TypeError("Image data of dtype {} cannot be converted to "
                            "float".format(self._A.dtype))

        if self._A.ndim == 3 and self._A.shape[-1] == 1:
            # If just one dimension assume scalar and apply colormap
            self._A = self._A[:, :, 0]

        if not (self._A.ndim == 2
                or self._A.ndim == 3 and self._A.shape[-1] in [3, 4]):
            raise TypeError("Invalid shape {} for image data"
                            .format(self._A.shape))

        if self._A.ndim == 3:
            # If the input data has values outside the valid range (after
            # normalisation), we issue a warning and then clip X to the bounds
            # - otherwise casting wraps extreme values, hiding outliers and
            # making reliable interpretation impossible.
            high = 255 if np.issubdtype(self._A.dtype, np.integer) else 1
            if self._A.min() < 0 or high < self._A.max():
                _log.warning(
                    'Clipping input data to the valid range for imshow with '
                    'RGB data ([0..1] for floats or [0..255] for integers).'
                )
                self._A = np.clip(self._A, 0, high)
            # Cast unsupported integer types to uint8
            if self._A.dtype != np.uint8 and np.issubdtype(self._A.dtype,
                                                           np.integer):
                self._A = self._A.astype(np.uint8)

        self._imcache = None
        self._rgbacache = None
        self.stale = True
