    def _draw_polygon(self):
        """Redraw the polygon based on the new vertex positions."""
        xs, ys = zip(*self._xys) if self._xys else ([], [])
        self._selection_artist.set_data(xs, ys)
        self._update_box()
        # Only show one tool handle at the start and end vertex of the polygon
        # if the polygon is completed or the user is locked on to the start
        # vertex.
        if (self._selection_completed
                or (len(self._xys) > 3
                    and self._xys[-1] == self._xys[0])):
            self._polygon_handles.set_data(xs[:-1], ys[:-1])
        else:
            self._polygon_handles.set_data(xs, ys)
        self.update()
