    def _make_paths_from_contour_generator(self):
        """Compute ``paths`` using C extension."""
        if self._paths is not None:
            return self._paths
        cg = self._contour_generator
        empty_path = Path(np.empty((0, 2)))
        vertices_and_codes = (
            map(cg.create_filled_contour, *self._get_lowers_and_uppers())
            if self.filled else
            map(cg.create_contour, self.levels))
        return [Path(np.concatenate(vs), np.concatenate(cs)) if len(vs) else empty_path
                for vs, cs in vertices_and_codes]
