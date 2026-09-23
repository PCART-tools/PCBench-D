    def get_flat_tri_mask(self, min_circle_ratio=0.01, rescale=True):
        """
        Eliminates excessively flat border triangles from the triangulation.

        Returns a mask *new_mask* which allows to clean the encapsulated
        triangulation from its border-located flat triangles
        (according to their :meth:`circle_ratios`).
        This mask is meant to be subsequently applied to the triangulation
        using :func:`matplotlib.tri.Triangulation.set_mask`.
        *new_mask* is an extension of the initial triangulation mask
        in the sense that an initially masked triangle will remain masked.

        The *new_mask* array is computed recursively; at each step flat
        triangles are removed only if they share a side with the current mesh
        border. Thus no new holes in the triangulated domain will be created.

        Parameters
        ----------
        min_circle_ratio : float, optional
            Border triangles with incircle/circumcircle radii ratio r/R will
            be removed if r/R < *min_circle_ratio*. Default value: 0.01
        rescale : boolean, optional
            If True, a rescaling will first be internally performed (based on
            :attr:`scale_factors` ), so that the (unmasked) triangles fit
            exactly inside a unit square mesh. This rescaling accounts for the
            difference of scale which might exist between the 2 axis. Default
            (and recommended) value is True.

        Returns
        -------
        new_mask : array-like of booleans
            Mask to apply to encapsulated triangulation.
            All the initially masked triangles remain masked in the
            *new_mask*.

        Notes
        -----
        The rationale behind this function is that a Delaunay
        triangulation - of an unstructured set of points - sometimes contains
        almost flat triangles at its border, leading to artifacts in plots
        (especially for high-resolution contouring).
        Masked with computed *new_mask*, the encapsulated
        triangulation would contain no more unmasked border triangles
        with a circle ratio below *min_circle_ratio*, thus improving the
        mesh quality for subsequent plots or interpolation.
        """
        # Recursively computes the mask_current_borders, true if a triangle is
        # at the border of the mesh OR touching the border through a chain of
        # invalid aspect ratio masked_triangles.
        ntri = self._triangulation.triangles.shape[0]
        mask_bad_ratio = self.circle_ratios(rescale) < min_circle_ratio

        current_mask = self._triangulation.mask
        if current_mask is None:
            current_mask = np.zeros(ntri, dtype=bool)
        valid_neighbors = np.copy(self._triangulation.neighbors)
        renum_neighbors = np.arange(ntri, dtype=np.int32)
        nadd = -1
        while nadd != 0:
            # The active wavefront is the triangles from the border (unmasked
            # but with a least 1 neighbor equal to -1
            wavefront = ((np.min(valid_neighbors, axis=1) == -1)
                         & ~current_mask)
            # The element from the active wavefront will be masked if their
            # circle ratio is bad.
            added_mask = np.logical_and(wavefront, mask_bad_ratio)
            current_mask = (added_mask | current_mask)
            nadd = np.sum(added_mask)

            # now we have to update the tables valid_neighbors
            valid_neighbors[added_mask, :] = -1
            renum_neighbors[added_mask] = -1
            valid_neighbors = np.where(valid_neighbors == -1, -1,
                                       renum_neighbors[valid_neighbors])

        return np.ma.filled(current_mask, True)
