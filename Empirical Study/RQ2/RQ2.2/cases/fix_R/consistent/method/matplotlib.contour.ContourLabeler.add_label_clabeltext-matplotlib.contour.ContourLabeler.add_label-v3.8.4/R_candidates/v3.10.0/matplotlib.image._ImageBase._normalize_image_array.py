    @staticmethod
    def _normalize_image_array(A):
        """
        Check validity of image-like input *A* and normalize it to a format suitable for
        Image subclasses.
        """
        A = cbook.safe_masked_invalid(A, copy=True)
        if A.dtype != np.uint8 and not np.can_cast(A.dtype, float, "same_kind"):
            raise TypeError(f"Image data of dtype {A.dtype} cannot be "
                            f"converted to float")
        if A.ndim == 3 and A.shape[-1] == 1:
            A = A.squeeze(-1)  # If just (M, N, 1), assume scalar and apply colormap.
        if not (A.ndim == 2 or A.ndim == 3 and A.shape[-1] in [3, 4]):
            raise TypeError(f"Invalid shape {A.shape} for image data")
        if A.ndim == 3:
            # If the input data has values outside the valid range (after
            # normalisation), we issue a warning and then clip X to the bounds
            # - otherwise casting wraps extreme values, hiding outliers and
            # making reliable interpretation impossible.
            high = 255 if np.issubdtype(A.dtype, np.integer) else 1
            if A.min() < 0 or high < A.max():
                _log.warning(
                    'Clipping input data to the valid range for imshow with '
                    'RGB data ([0..1] for floats or [0..255] for integers). '
                    'Got range [%s..%s].',
                    A.min(), A.max()
                )
                A = np.clip(A, 0, high)
            # Cast unsupported integer types to uint8
            if A.dtype != np.uint8 and np.issubdtype(A.dtype, np.integer):
                A = A.astype(np.uint8)
        return A
