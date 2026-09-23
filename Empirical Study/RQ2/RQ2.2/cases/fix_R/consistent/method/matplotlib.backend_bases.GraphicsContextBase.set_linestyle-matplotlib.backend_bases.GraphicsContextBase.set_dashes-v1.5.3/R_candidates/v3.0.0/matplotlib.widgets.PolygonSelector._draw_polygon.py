    def _draw_polygon(self):
        """Redraw the polygon based on the new vertex positions."""
        self.line.set_data(self._xs, self._ys)
        # Only show one tool handle at the start and end vertex of the polygon
        # if the polygon is completed or the user is locked on to the start
        # vertex.
        if (self._polygon_completed
                or (len(self._xs) > 3
                    and self._xs[-1] == self._xs[0]
                    and self._ys[-1] == self._ys[0])):
            self._polygon_handles.set_data(self._xs[:-1], self._ys[:-1])
        else:
            self._polygon_handles.set_data(self._xs, self._ys)
        self.update()
