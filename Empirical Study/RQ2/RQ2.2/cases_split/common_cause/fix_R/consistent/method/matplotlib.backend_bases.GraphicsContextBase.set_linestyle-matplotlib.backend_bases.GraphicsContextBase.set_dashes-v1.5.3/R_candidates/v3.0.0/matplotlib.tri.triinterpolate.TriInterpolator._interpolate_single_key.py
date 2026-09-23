    def _interpolate_single_key(self, return_key, tri_index, x, y):
        """
        Performs the interpolation at points belonging to the triangulation
        (inside an unmasked triangles).

        Parameters
        ----------
        return_index : string key from {'z', 'dzdx', 'dzdy'}
            Identifies the requested values (z or its derivatives)
        tri_index : 1d integer array
            Valid triangle index (-1 prohibited)
        x, y : 1d arrays, same shape as `tri_index`
            Valid locations where interpolation is requested.

        Returns
        -------
        ret : 1-d array
            Returned array of the same size as *tri_index*
        """
        raise NotImplementedError("TriInterpolator subclasses" +
                                  "should implement _interpolate_single_key!")
