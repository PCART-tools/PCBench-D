    @property
    def scale_factors(self):
        """
        Factors to rescale the triangulation into a unit square.

        Returns *k*, tuple of 2 scale factors.

        Returns
        -------
        k : tuple of 2 floats (kx, ky)
            Tuple of floats that would rescale the triangulation :
            ``[triangulation.x * kx, triangulation.y * ky]``
            fits exactly inside a unit square.

        """
        compressed_triangles = self._triangulation.get_masked_triangles()
        node_used = (np.bincount(np.ravel(compressed_triangles),
                                 minlength=self._triangulation.x.size) != 0)
        return (1 / np.ptp(self._triangulation.x[node_used]),
                1 / np.ptp(self._triangulation.y[node_used]))
