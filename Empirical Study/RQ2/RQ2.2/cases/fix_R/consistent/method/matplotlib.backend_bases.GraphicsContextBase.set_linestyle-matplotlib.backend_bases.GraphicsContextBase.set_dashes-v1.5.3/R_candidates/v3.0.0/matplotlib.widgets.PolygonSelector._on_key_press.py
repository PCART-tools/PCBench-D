    def _on_key_press(self, event):
        """Key press event handler"""
        # Remove the pending vertex if entering the 'move_vertex' or
        # 'move_all' mode
        if (not self._polygon_completed
                and ('move_vertex' in self.state or 'move_all' in self.state)):
            self._xs, self._ys = self._xs[:-1], self._ys[:-1]
            self._draw_polygon()
