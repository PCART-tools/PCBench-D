    def get_window_extent(self, renderer=None):
        """
        Return the `Bbox` bounding the text and arrow, in display units.

        Parameters
        ----------
        renderer : Renderer, optional
            A renderer is needed to compute the bounding box.  If the artist
            has already been drawn, the renderer is cached; thus, it is only
            necessary to pass this argument when calling `get_window_extent`
            before the first `draw`.  In practice, it is usually easier to
            trigger a draw first (e.g. by saving the figure).
        """
        # This block is the same as in Text.get_window_extent, but we need to
        # set the renderer before calling update_positions().
        if not self.get_visible():
            return Bbox.unit()
        if renderer is not None:
            self._renderer = renderer
        if self._renderer is None:
            self._renderer = self.figure._cachedRenderer
        if self._renderer is None:
            raise RuntimeError('Cannot get window extent w/o renderer')

        self.update_positions(self._renderer)

        text_bbox = Text.get_window_extent(self)
        bboxes = [text_bbox]

        if self.arrow_patch is not None:
            bboxes.append(self.arrow_patch.get_window_extent())

        return Bbox.union(bboxes)
