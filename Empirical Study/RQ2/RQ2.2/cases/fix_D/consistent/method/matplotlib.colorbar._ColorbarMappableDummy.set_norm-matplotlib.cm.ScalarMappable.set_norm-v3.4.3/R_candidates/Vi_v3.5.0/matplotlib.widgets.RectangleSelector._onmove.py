    def _onmove(self, event):
        """Motion notify event handler."""

        state = self._state | self._default_state
        # resize an existing shape
        if self._active_handle and self._active_handle != 'C':
            x0, x1, y0, y1 = self._extents_on_press
            size_on_press = [x1 - x0, y1 - y0]
            center = [x0 + size_on_press[0] / 2, y0 + size_on_press[1] / 2]
            dx = event.xdata - self._eventpress.xdata
            dy = event.ydata - self._eventpress.ydata

            # change sign of relative changes to simplify calculation
            # Switch variables so that only x1 and/or y1 are updated on move
            x_factor = y_factor = 1
            if 'W' in self._active_handle:
                x_factor *= -1
                dx *= x_factor
                x0 = x1
            if 'S' in self._active_handle:
                y_factor *= -1
                dy *= y_factor
                y0 = y1

            # Keeping the center fixed
            if 'center' in state:
                if 'square' in state:
                    # Force the same change in dx and dy
                    if self._active_handle in ['E', 'W']:
                        # using E, W handle we need to update dy accordingly
                        dy = dx
                    elif self._active_handle in ['S', 'N']:
                        # using S, N handle, we need to update dx accordingly
                        dx = dy
                    else:
                        dx = dy = max(dx, dy, key=abs)

                # new half-width and half-height
                hw = size_on_press[0] / 2 + dx
                hh = size_on_press[1] / 2 + dy

                if 'square' not in state:
                    # cancel changes in perpendicular direction
                    if self._active_handle in ['E', 'W']:
                        hh = size_on_press[1] / 2
                    if self._active_handle in ['N', 'S']:
                        hw = size_on_press[0] / 2

                x0, x1, y0, y1 = (center[0] - hw, center[0] + hw,
                                  center[1] - hh, center[1] + hh)

            else:
                # Keeping the opposite corner/edge fixed
                if 'square' in state:
                    dx = dy = max(dx, dy, key=abs)
                    x1 = x0 + x_factor * (dx + size_on_press[0])
                    y1 = y0 + y_factor * (dy + size_on_press[1])
                else:
                    if self._active_handle in ['E', 'W'] + self._corner_order:
                        x1 = event.xdata
                    if self._active_handle in ['N', 'S'] + self._corner_order:
                        y1 = event.ydata

        # move existing shape
        elif (self._active_handle == 'C' or
              (self.drag_from_anywhere and self._contains(event)) and
              self._extents_on_press is not None):
            x0, x1, y0, y1 = self._extents_on_press
            dx = event.xdata - self._eventpress.xdata
            dy = event.ydata - self._eventpress.ydata
            x0 += dx
            x1 += dx
            y0 += dy
            y1 += dy

        # new shape
        else:
            # Don't create a new rectangle if there is already one when
            # ignore_event_outside=True
            if self.ignore_event_outside and self._selection_completed:
                return
            center = [self._eventpress.xdata, self._eventpress.ydata]
            center_pix = [self._eventpress.x, self._eventpress.y]
            dx = (event.xdata - center[0]) / 2.
            dy = (event.ydata - center[1]) / 2.

            # square shape
            if 'square' in state:
                dx_pix = abs(event.x - center_pix[0])
                dy_pix = abs(event.y - center_pix[1])
                if not dx_pix:
                    return
                maxd = max(abs(dx_pix), abs(dy_pix))
                if abs(dx_pix) < maxd:
                    dx *= maxd / (abs(dx_pix) + 1e-6)
                if abs(dy_pix) < maxd:
                    dy *= maxd / (abs(dy_pix) + 1e-6)

            # from center
            if 'center' in state:
                dx *= 2
                dy *= 2

            # from corner
            else:
                center[0] += dx
                center[1] += dy

            x0, x1, y0, y1 = (center[0] - dx, center[0] + dx,
                              center[1] - dy, center[1] + dy)

        self.extents = x0, x1, y0, y1
