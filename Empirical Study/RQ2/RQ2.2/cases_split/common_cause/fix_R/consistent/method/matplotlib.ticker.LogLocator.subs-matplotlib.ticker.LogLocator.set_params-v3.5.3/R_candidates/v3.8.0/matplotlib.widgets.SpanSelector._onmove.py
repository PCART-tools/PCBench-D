    def _onmove(self, event):
        """Motion notify event handler."""

        xdata, ydata = self._get_data_coords(event)
        if self.direction == 'horizontal':
            v = xdata
            vpress = self._eventpress.xdata
        else:
            v = ydata
            vpress = self._eventpress.ydata

        # move existing span
        # When "dragging from anywhere", `self._active_handle` is set to 'C'
        # (match notation used in the RectangleSelector)
        if self._active_handle == 'C' and self._extents_on_press is not None:
            vmin, vmax = self._extents_on_press
            dv = v - vpress
            vmin += dv
            vmax += dv

        # resize an existing shape
        elif self._active_handle and self._active_handle != 'C':
            vmin, vmax = self._extents_on_press
            if self._active_handle == 'min':
                vmin = v
            else:
                vmax = v
        # new shape
        else:
            # Don't create a new span if there is already one when
            # ignore_event_outside=True
            if self.ignore_event_outside and self._selection_completed:
                return
            vmin, vmax = vpress, v
            if vmin > vmax:
                vmin, vmax = vmax, vmin

        self.extents = vmin, vmax

        if self.onmove_callback is not None:
            self.onmove_callback(vmin, vmax)

        return False
