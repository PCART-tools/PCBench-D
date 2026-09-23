    def push_current(self):
        """Push the current view limits and position onto the stack."""
        views = []
        pos = []
        for a in self.canvas.figure.get_axes():
            views.append(a._get_view())
            # Store both the original and modified positions
            pos.append((
                a.get_position(True).frozen(),
                a.get_position().frozen()))
        self._views.push(views)
        self._positions.push(pos)
        self.set_history_buttons()
