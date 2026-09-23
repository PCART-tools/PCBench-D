    def set_mask(self, mask):
        """
        Set or clear the mask array.

        Parameters
        ----------
        mask : None or bool array of length ntri
        """
        if mask is None:
            self.mask = None
        else:
            self.mask = np.asarray(mask, dtype=bool)
            if self.mask.shape != (self.triangles.shape[0],):
                raise ValueError('mask array must have same length as '
                                 'triangles array')

        # Set mask in C++ Triangulation.
        if self._cpp_triangulation is not None:
            self._cpp_triangulation.set_mask(self.mask)

        # Clear derived fields so they are recalculated when needed.
        self._edges = None
        self._neighbors = None

        # Recalculate TriFinder if it exists.
        if self._trifinder is not None:
            self._trifinder._initialize()
