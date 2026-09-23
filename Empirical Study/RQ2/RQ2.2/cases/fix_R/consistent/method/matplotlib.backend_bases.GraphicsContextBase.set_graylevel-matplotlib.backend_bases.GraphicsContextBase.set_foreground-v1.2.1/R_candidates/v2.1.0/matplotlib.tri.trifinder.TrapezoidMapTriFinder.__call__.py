    def __call__(self, x, y):
        """
        Return an array containing the indices of the triangles in which the
        specified x,y points lie, or -1 for points that do not lie within a
        triangle.

        *x*, *y* are array_like x and y coordinates of the same shape and any
        number of dimensions.

        Returns integer array with the same shape and *x* and *y*.
        """
        x = np.asarray(x, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        if x.shape != y.shape:
            raise ValueError("x and y must be array-like with the same shape")

        # C++ does the heavy lifting, and expects 1D arrays.
        indices = (self._cpp_trifinder.find_many(x.ravel(), y.ravel())
                   .reshape(x.shape))
        return indices
