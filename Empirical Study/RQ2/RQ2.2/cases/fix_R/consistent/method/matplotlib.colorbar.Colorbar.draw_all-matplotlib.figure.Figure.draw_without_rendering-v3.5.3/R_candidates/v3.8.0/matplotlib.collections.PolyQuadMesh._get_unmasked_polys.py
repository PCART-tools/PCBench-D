    def _get_unmasked_polys(self):
        """Get the unmasked regions using the coordinates and array"""
        # mask(X) | mask(Y)
        mask = np.any(np.ma.getmaskarray(self._coordinates), axis=-1)

        # We want the shape of the polygon, which is the corner of each X/Y array
        mask = (mask[0:-1, 0:-1] | mask[1:, 1:] | mask[0:-1, 1:] | mask[1:, 0:-1])

        if (getattr(self, "_deprecated_compression", False) and
                np.any(self._original_mask)):
            return ~(mask | self._original_mask)
        # Take account of the array data too, temporarily avoiding
        # the compression warning and resetting the variable after the call
        with cbook._setattr_cm(self, _deprecated_compression=False):
            arr = self.get_array()
        if arr is not None:
            arr = np.ma.getmaskarray(arr)
            if arr.ndim == 3:
                # RGB(A) case
                mask |= np.any(arr, axis=-1)
            elif arr.ndim == 2:
                mask |= arr
            else:
                mask |= arr.reshape(self._coordinates[:-1, :-1, :].shape[:2])
        return ~mask
