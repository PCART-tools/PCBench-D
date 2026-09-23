    @axes.setter
    def axes(self, new_axes):
        if (new_axes is not None and self._axes is not None
                and new_axes != self._axes):
            raise ValueError("Can not reset the Axes. You are probably trying to reuse "
                             "an artist in more than one Axes which is not supported")
        self._axes = new_axes
        if new_axes is not None and new_axes is not self:
            self.stale_callback = _stale_axes_callback
