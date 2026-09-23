    def clear(self):
        """Uncheck all checkboxes."""

        self._checks.set_facecolor(['none'] * len(self._active_check_colors))

        if hasattr(self, '_lines'):
            for l1, l2 in self._lines:
                l1.set_visible(False)
                l2.set_visible(False)

        if self.drawon:
            self.canvas.draw()

        if self.eventson:
            # Call with no label, as all checkboxes are being cleared.
            self._observers.process('clicked', None)
