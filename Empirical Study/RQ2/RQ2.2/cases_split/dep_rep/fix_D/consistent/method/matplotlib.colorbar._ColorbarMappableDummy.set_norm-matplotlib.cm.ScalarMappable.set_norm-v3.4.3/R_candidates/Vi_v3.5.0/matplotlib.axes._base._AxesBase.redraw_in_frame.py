    def redraw_in_frame(self):
        """
        Efficiently redraw Axes data, but not axis ticks, labels, etc.

        This method can only be used after an initial draw which caches the
        renderer.
        """
        if self.figure._cachedRenderer is None:
            raise AttributeError("redraw_in_frame can only be used after an "
                                 "initial draw which caches the renderer")
        with ExitStack() as stack:
            for artist in [*self._get_axis_list(),
                           self.title, self._left_title, self._right_title]:
                stack.enter_context(artist._cm_set(visible=False))
            self.draw(self.figure._cachedRenderer)
