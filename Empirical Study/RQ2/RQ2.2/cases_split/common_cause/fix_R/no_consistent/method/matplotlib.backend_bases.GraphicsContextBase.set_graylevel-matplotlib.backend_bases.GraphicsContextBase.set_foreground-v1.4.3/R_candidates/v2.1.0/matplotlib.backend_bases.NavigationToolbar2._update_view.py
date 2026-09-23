    def _update_view(self):
        """Update the viewlim and position from the view and
        position stack for each axes.
        """

        views = self._views()
        if views is None:
            return
        pos = self._positions()
        if pos is None:
            return
        for i, a in enumerate(self.canvas.figure.get_axes()):
            a._set_view(views[i])
            # Restore both the original and modified positions
            a.set_position(pos[i][0], 'original')
            a.set_position(pos[i][1], 'active')

        self.canvas.draw_idle()
