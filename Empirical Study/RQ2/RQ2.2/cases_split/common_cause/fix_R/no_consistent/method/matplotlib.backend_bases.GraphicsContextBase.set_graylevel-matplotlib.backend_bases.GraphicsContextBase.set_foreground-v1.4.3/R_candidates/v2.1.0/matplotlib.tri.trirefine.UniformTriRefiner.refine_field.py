    def refine_field(self, z, triinterpolator=None, subdiv=3):
        """
        Refines a field defined on the encapsulated triangulation.

        Returns *refi_tri* (refined triangulation), *refi_z* (interpolated
        values of the field at the node of the refined triangulation).

        Parameters
        ----------
        z : 1d-array-like of length ``n_points``
            Values of the field to refine, defined at the nodes of the
            encapsulated triangulation. (``n_points`` is the number of points
            in the initial triangulation)
        triinterpolator : :class:`~matplotlib.tri.TriInterpolator`, optional
            Interpolator used for field interpolation. If not specified,
            a :class:`~matplotlib.tri.CubicTriInterpolator` will
            be used.
        subdiv : integer, optional
            Recursion level for the subdivision. Defaults to 3.
            Each triangle will be divided into ``4**subdiv`` child triangles.

        Returns
        -------
        refi_tri : :class:`~matplotlib.tri.Triangulation` object
                     The returned refined triangulation
        refi_z : 1d array of length: *refi_tri* node count.
                   The returned interpolated field (at *refi_tri* nodes)
        """
        if triinterpolator is None:
            interp = matplotlib.tri.CubicTriInterpolator(
                self._triangulation, z)
        else:
            if not isinstance(triinterpolator,
                              matplotlib.tri.TriInterpolator):
                raise ValueError("Expected a TriInterpolator object")
            interp = triinterpolator

        refi_tri, found_index = self.refine_triangulation(
            subdiv=subdiv, return_tri_index=True)
        refi_z = interp._interpolate_multikeys(
            refi_tri.x, refi_tri.y, tri_index=found_index)[0]
        return refi_tri, refi_z
