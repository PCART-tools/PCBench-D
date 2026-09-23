    def _release(self, event):
        """Button release event handler."""
        self._set_cursor(False)
        # self._pressv is deprecated but we still need to maintain it
        self._pressv = None

        if not self._interactive:
            self._selection_artist.set_visible(False)

        if (self._active_handle is None and self._selection_completed and
                self.ignore_event_outside):
            return

        vmin, vmax = self.extents
        span = vmax - vmin

        if span <= self.minspan:
            # Remove span and set self._selection_completed = False
            self.set_visible(False)
            if self._selection_completed:
                # Call onselect, only when the span is already existing
                self.onselect(vmin, vmax)
            self._selection_completed = False
        else:
            self.onselect(vmin, vmax)
            self._selection_completed = True

        self.update()

        self._active_handle = None

        return False
