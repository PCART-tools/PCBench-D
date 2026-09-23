    def _get_allsegs_and_allkinds(self):
        """Compute ``allsegs`` and ``allkinds`` using C extension."""
        allsegs = []
        allkinds = []
        if self.filled:
            lowers, uppers = self._get_lowers_and_uppers()
            for level, level_upper in zip(lowers, uppers):
                vertices, kinds = \
                    self._contour_generator.create_filled_contour(
                        level, level_upper)
                allsegs.append(vertices)
                allkinds.append(kinds)
        else:
            for level in self.levels:
                vertices, kinds = self._contour_generator.create_contour(level)
                allsegs.append(vertices)
                allkinds.append(kinds)
        return allsegs, allkinds
