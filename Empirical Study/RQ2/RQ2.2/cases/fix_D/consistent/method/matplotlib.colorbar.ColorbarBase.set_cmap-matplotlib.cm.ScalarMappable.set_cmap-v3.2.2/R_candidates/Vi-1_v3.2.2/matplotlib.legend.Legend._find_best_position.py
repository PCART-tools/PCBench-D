    def _find_best_position(self, width, height, renderer, consider=None):
        """
        Determine the best location to place the legend.

        *consider* is a list of ``(x, y)`` pairs to consider as a potential
        lower-left corner of the legend. All are display coords.
        """
        # should always hold because function is only called internally
        assert self.isaxes

        start_time = time.perf_counter()

        verts, bboxes, lines, offsets = self._auto_legend_data()

        bbox = Bbox.from_bounds(0, 0, width, height)
        if consider is None:
            consider = [self._get_anchored_bbox(x, bbox,
                                                self.get_bbox_to_anchor(),
                                                renderer)
                        for x in range(1, len(self.codes))]

        candidates = []
        for idx, (l, b) in enumerate(consider):
            legendBox = Bbox.from_bounds(l, b, width, height)
            badness = 0
            # XXX TODO: If markers are present, it would be good to
            # take them into account when checking vertex overlaps in
            # the next line.
            badness = (legendBox.count_contains(verts)
                       + legendBox.count_contains(offsets)
                       + legendBox.count_overlaps(bboxes)
                       + sum(line.intersects_bbox(legendBox, filled=False)
                             for line in lines))
            if badness == 0:
                return l, b
            # Include the index to favor lower codes in case of a tie.
            candidates.append((badness, idx, (l, b)))

        _, _, (l, b) = min(candidates)

        if self._loc_used_default and time.perf_counter() - start_time > 1:
            cbook._warn_external(
                'Creating legend with loc="best" can be slow with large '
                'amounts of data.')

        return l, b
