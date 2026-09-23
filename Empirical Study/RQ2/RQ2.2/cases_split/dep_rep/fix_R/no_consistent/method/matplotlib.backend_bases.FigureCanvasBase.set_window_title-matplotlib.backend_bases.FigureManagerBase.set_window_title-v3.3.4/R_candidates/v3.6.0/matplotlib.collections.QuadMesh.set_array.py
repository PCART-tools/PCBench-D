    def set_array(self, A):
        """
        Set the data values.

        Parameters
        ----------
        A : (M, N) array-like or M*N array-like
            If the values are provided as a 2D grid, the shape must match the
            coordinates grid. If the values are 1D, they are reshaped to 2D.
            M, N follow from the coordinates grid, where the coordinates grid
            shape is (M, N) for 'gouraud' *shading* and (M+1, N+1) for 'flat'
            shading.
        """
        height, width = self._coordinates.shape[0:-1]
        misshapen_data = False
        faulty_data = False

        if self._shading == 'flat':
            h, w = height-1, width-1
        else:
            h, w = height, width

        if A is not None:
            shape = np.shape(A)
            if len(shape) == 1:
                if shape[0] != (h*w):
                    faulty_data = True
            elif shape != (h, w):
                if np.prod(shape) == (h * w):
                    misshapen_data = True
                else:
                    faulty_data = True

            if misshapen_data:
                _api.warn_deprecated(
                    "3.5", message=f"For X ({width}) and Y ({height}) "
                    f"with {self._shading} shading, the expected shape of "
                    f"A is ({h}, {w}). Passing A ({A.shape}) is deprecated "
                    "since %(since)s and will become an error %(removal)s.")

            if faulty_data:
                raise TypeError(
                    f"Dimensions of A {A.shape} are incompatible with "
                    f"X ({width}) and/or Y ({height})")

        return super().set_array(A)
