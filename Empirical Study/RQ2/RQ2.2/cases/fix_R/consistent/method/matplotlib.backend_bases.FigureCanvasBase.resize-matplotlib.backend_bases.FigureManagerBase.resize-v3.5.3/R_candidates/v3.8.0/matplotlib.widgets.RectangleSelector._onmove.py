    def _onmove(self, event):
        """
        Motion notify event handler.

        This can do one of four things:
        - Translate
        - Rotate
        - Re-size
        - Continue the creation of a new shape
        """
        eventpress = self._eventpress
        # The calculations are done for rotation at zero: we apply inverse
        # transformation to events except when we rotate and move
        state = self._state
        rotate = 'rotate' in state and self._active_handle in self._corner_order
        move = self._active_handle == 'C'
        resize = self._active_handle and not move

        xdata, ydata = self._get_data_coords(event)
        if resize:
            inv_tr = self._get_rotation_transform().inverted()
            xdata, ydata = inv_tr.transform([xdata, ydata])
            eventpress.xdata, eventpress.ydata = inv_tr.transform(
                (eventpress.xdata, eventpress.ydata))

        dx = xdata - eventpress.xdata
        dy = ydata - eventpress.ydata
        # refmax is used when moving the corner handle with the square state
        # and is the maximum between refx and refy
        refmax = None
        if self._use_data_coordinates:
            refx, refy = dx, dy
        else:
            # Get dx/dy in display coordinates
            refx = event.x - eventpress.x
            refy = event.y - eventpress.y

        x0, x1, y0, y1 = self._extents_on_press
        # rotate an existing shape
        if rotate:
            # calculate angle abc
            a = (eventpress.xdata, eventpress.ydata)
            b = self.center
            c = (xdata, ydata)
            angle = (np.arctan2(c[1]-b[1], c[0]-b[0]) -
                     np.arctan2(a[1]-b[1], a[0]-b[0]))
            self.rotation = np.rad2deg(self._rotation_on_press + angle)

        elif resize:
            size_on_press = [x1 - x0, y1 - y0]
            center = (x0 + size_on_press[0] / 2, y0 + size_on_press[1] / 2)

            # Keeping the center fixed
            if 'center' in state:
                # hh, hw are half-height and half-width
                if 'square' in state:
                    # when using a corner, find which reference to use
                    if self._active_handle in self._corner_order:
                        refmax = max(refx, refy, key=abs)
                    if self._active_handle in ['E', 'W'] or refmax == refx:
                        hw = xdata - center[0]
                        hh = hw / self._aspect_ratio_correction
                    else:
                        hh = ydata - center[1]
                        hw = hh * self._aspect_ratio_correction
                else:
                    hw = size_on_press[0] / 2
                    hh = size_on_press[1] / 2
                    # cancel changes in perpendicular direction
                    if self._active_handle in ['E', 'W'] + self._corner_order:
                        hw = abs(xdata - center[0])
                    if self._active_handle in ['N', 'S'] + self._corner_order:
                        hh = abs(ydata - center[1])

                x0, x1, y0, y1 = (center[0] - hw, center[0] + hw,
                                  center[1] - hh, center[1] + hh)

            else:
                # change sign of relative changes to simplify calculation
                # Switch variables so that x1 and/or y1 are updated on move
                if 'W' in self._active_handle:
                    x0 = x1
                if 'S' in self._active_handle:
                    y0 = y1
                if self._active_handle in ['E', 'W'] + self._corner_order:
                    x1 = xdata
                if self._active_handle in ['N', 'S'] + self._corner_order:
                    y1 = ydata
                if 'square' in state:
                    # when using a corner, find which reference to use
                    if self._active_handle in self._corner_order:
                        refmax = max(refx, refy, key=abs)
                    if self._active_handle in ['E', 'W'] or refmax == refx:
                        sign = np.sign(ydata - y0)
                        y1 = y0 + sign * abs(x1 - x0) / self._aspect_ratio_correction
                    else:
                        sign = np.sign(xdata - x0)
                        x1 = x0 + sign * abs(y1 - y0) * self._aspect_ratio_correction

        elif move:
            x0, x1, y0, y1 = self._extents_on_press
            dx = xdata - eventpress.xdata
            dy = ydata - eventpress.ydata
            x0 += dx
            x1 += dx
            y0 += dy
            y1 += dy

        else:
            # Create a new shape
            self._rotation = 0
            # Don't create a new rectangle if there is already one when
            # ignore_event_outside=True
            if ((self.ignore_event_outside and self._selection_completed) or
                    not self._allow_creation):
                return
            center = [eventpress.xdata, eventpress.ydata]
            dx = (xdata - center[0]) / 2
            dy = (ydata - center[1]) / 2

            # square shape
            if 'square' in state:
                refmax = max(refx, refy, key=abs)
                if refmax == refx:
                    dy = np.sign(dy) * abs(dx) / self._aspect_ratio_correction
                else:
                    dx = np.sign(dx) * abs(dy) * self._aspect_ratio_correction

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
