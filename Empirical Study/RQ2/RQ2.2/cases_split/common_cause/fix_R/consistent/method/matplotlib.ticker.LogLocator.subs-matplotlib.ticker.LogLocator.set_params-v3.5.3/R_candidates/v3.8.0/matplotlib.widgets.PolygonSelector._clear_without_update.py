    def _clear_without_update(self):
        self._selection_completed = False
        self._xys = [(0, 0)]
        self._draw_polygon_without_update()
