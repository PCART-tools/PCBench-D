    def _find_nearest_contour(self, xy, indices=None):
        """
        Find the point in the unfilled contour plot that is closest (in screen
        space) to point *xy*.

        Parameters
        ----------
        xy : tuple[float, float]
            The reference point (in screen space).
        indices : list of int or None, default: None
            Indices of contour levels to consider.  If None (the default), all levels
            are considered.

        Returns
        -------
        idx_level_min : int
            The index of the contour level closest to *xy*.
        idx_vtx_min : int
            The index of the `.Path` segment closest to *xy* (at that level).
        proj : (float, float)
            The point in the contour plot closest to *xy*.
        """

        # Convert each contour segment to pixel coordinates and then compare the given
        # point to those coordinates for each contour. This is fast enough in normal
        # cases, but speedups may be possible.

        if self.filled:
            raise ValueError("Method does not support filled contours")

        if indices is None:
            indices = range(len(self._paths))

        d2min = np.inf
        idx_level_min = idx_vtx_min = proj_min = None

        for idx_level in indices:
            path = self._paths[idx_level]
            if not len(path.vertices):
                continue
            lc = self.get_transform().transform(path.vertices)
            d2, proj, leg = _find_closest_point_on_path(lc, xy)
            if d2 < d2min:
                d2min = d2
                idx_level_min = idx_level
                idx_vtx_min = leg[1]
                proj_min = proj

        return idx_level_min, idx_vtx_min, proj_min
