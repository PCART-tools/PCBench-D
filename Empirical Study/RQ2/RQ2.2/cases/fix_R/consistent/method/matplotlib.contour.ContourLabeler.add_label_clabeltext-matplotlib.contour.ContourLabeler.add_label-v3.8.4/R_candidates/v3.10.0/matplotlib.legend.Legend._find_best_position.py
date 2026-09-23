    def _find_best_position(self, width, height, renderer):
        """Determine the best location to place the legend."""
        assert self.isaxes  # always holds, as this is only called internally

        start_time = time.perf_counter()

        bboxes, lines, offsets = self._auto_legend_data()

        bbox = Bbox.from_bounds(0, 0, width, height)

        candidates = []
        for idx in range(1, len(self.codes)):
            l, b = self._get_anchored_bbox(idx, bbox,
                                           self.get_bbox_to_anchor(),
                                           renderer)
            legendBox = Bbox.from_bounds(l, b, width, height)
            # XXX TODO: If markers are present, it would be good to take them
            # into account when checking vertex overlaps in the next line.
            badness = (sum(legendBox.count_contains(line.vertices)
                           for line in lines)
                       + legendBox.count_contains(offsets)
                       + legendBox.count_overlaps(bboxes)
                       + sum(line.intersects_bbox(legendBox, filled=False)
                             for line in lines))
            # Include the index to favor lower codes in case of a tie.
            candidates.append((badness, idx, (l, b)))
            if badness == 0:
                break

        _, _, (l, b) = min(candidates)

        if self._loc_used_default and time.perf_counter() - start_time > 1:
            _api.warn_external(
                'Creating legend with loc="best" can be slow with large '
                'amounts of data.')

        return l, b
