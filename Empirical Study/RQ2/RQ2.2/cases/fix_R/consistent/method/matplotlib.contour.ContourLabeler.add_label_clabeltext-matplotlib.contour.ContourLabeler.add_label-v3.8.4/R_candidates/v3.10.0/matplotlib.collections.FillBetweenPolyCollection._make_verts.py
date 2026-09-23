    def _make_verts(self, t, f1, f2, where):
        """
        Make verts that can be forwarded to `.PolyCollection`.
        """
        self._validate_shapes(self.t_direction, self._f_direction, t, f1, f2)

        where = self._get_data_mask(t, f1, f2, where)
        t, f1, f2 = np.broadcast_arrays(np.atleast_1d(t), f1, f2, subok=True)

        self._bbox = transforms.Bbox.null()
        self._bbox.update_from_data_xy(self._fix_pts_xy_order(np.concatenate([
            np.stack((t[where], f[where]), axis=-1) for f in (f1, f2)])))

        return [
            self._make_verts_for_region(t, f1, f2, idx0, idx1)
            for idx0, idx1 in cbook.contiguous_regions(where)
        ]
