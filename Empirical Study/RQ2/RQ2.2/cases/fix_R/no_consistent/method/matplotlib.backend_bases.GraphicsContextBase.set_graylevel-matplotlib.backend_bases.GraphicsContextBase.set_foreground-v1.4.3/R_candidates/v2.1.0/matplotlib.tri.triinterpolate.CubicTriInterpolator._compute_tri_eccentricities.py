    @staticmethod
    def _compute_tri_eccentricities(tris_pts):
        """
        Computes triangle eccentricities

        Parameters
        ----------
        tris_pts : array like of dim 3 (shape: (nx,3,2))
                   Coordinates of the triangles apexes.

        Returns
        -------
        ecc : array like of dim 2 (shape: (nx,3))
              The so-called eccentricity parameters [1] needed for
              HCT triangular element.
        """
        a = np.expand_dims(tris_pts[:, 2, :]-tris_pts[:, 1, :], axis=2)
        b = np.expand_dims(tris_pts[:, 0, :]-tris_pts[:, 2, :], axis=2)
        c = np.expand_dims(tris_pts[:, 1, :]-tris_pts[:, 0, :], axis=2)
        # Do not use np.squeeze, this is dangerous if only one triangle
        # in the triangulation...
        dot_a = _prod_vectorized(_transpose_vectorized(a), a)[:, 0, 0]
        dot_b = _prod_vectorized(_transpose_vectorized(b), b)[:, 0, 0]
        dot_c = _prod_vectorized(_transpose_vectorized(c), c)[:, 0, 0]
        # Note that this line will raise a warning for dot_a, dot_b or dot_c
        # zeros, but we choose not to support triangles with duplicate points.
        return _to_matrix_vectorized([[(dot_c-dot_b) / dot_a],
                                      [(dot_a-dot_c) / dot_b],
                                      [(dot_b-dot_a) / dot_c]])
