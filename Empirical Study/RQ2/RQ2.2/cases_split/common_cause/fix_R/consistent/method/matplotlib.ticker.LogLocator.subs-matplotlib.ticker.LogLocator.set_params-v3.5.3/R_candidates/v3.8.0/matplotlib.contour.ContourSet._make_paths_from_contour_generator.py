    def _make_paths_from_contour_generator(self):
        """Compute ``paths`` using C extension."""
        if self._paths is not None:
            return self._paths
        paths = []
        empty_path = Path(np.empty((0, 2)))
        if self.filled:
            lowers, uppers = self._get_lowers_and_uppers()
            for level, level_upper in zip(lowers, uppers):
                vertices, kinds = \
                    self._contour_generator.create_filled_contour(
                        level, level_upper)
                paths.append(Path(np.concatenate(vertices), np.concatenate(kinds))
                             if len(vertices) else empty_path)
        else:
            for level in self.levels:
                vertices, kinds = self._contour_generator.create_contour(level)
                paths.append(Path(np.concatenate(vertices), np.concatenate(kinds))
                             if len(vertices) else empty_path)
        return paths
