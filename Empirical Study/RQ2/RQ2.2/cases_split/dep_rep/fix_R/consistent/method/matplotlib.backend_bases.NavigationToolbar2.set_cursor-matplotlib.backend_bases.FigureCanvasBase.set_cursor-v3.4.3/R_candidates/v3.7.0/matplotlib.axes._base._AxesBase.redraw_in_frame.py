    def redraw_in_frame(self):
        """
        Efficiently redraw Axes data, but not axis ticks, labels, etc.
        """
        with ExitStack() as stack:
            for artist in [*self._axis_map.values(),
                           self.title, self._left_title, self._right_title]:
                stack.enter_context(artist._cm_set(visible=False))
            self.draw(self.figure.canvas.get_renderer())
