    def drag_pan(self, button, key, x, y):
        """
        Called when the mouse moves during a pan operation.

        Parameters
        ----------
        button : `.MouseButton`
            The pressed mouse button.
        key : str or None
            The pressed key, if any.
        x, y : float
            The mouse coordinates in display coords.

        Notes
        -----
        This is intended to be overridden by new projection types.
        """
        def format_deltas(key, dx, dy):
            if key == 'control':
                if abs(dx) > abs(dy):
                    dy = dx
                else:
                    dx = dy
            elif key == 'x':
                dy = 0
            elif key == 'y':
                dx = 0
            elif key == 'shift':
                if 2 * abs(dx) < abs(dy):
                    dx = 0
                elif 2 * abs(dy) < abs(dx):
                    dy = 0
                elif abs(dx) > abs(dy):
                    dy = dy / abs(dy) * abs(dx)
                else:
                    dx = dx / abs(dx) * abs(dy)
            return dx, dy

        p = self._pan_start
        dx = x - p.x
        dy = y - p.y
        if dx == dy == 0:
            return
        if button == 1:
            dx, dy = format_deltas(key, dx, dy)
            result = p.bbox.translated(-dx, -dy).transformed(p.trans_inverse)
        elif button == 3:
            try:
                dx = -dx / self.bbox.width
                dy = -dy / self.bbox.height
                dx, dy = format_deltas(key, dx, dy)
                if self.get_aspect() != 'auto':
                    dx = dy = 0.5 * (dx + dy)
                alpha = np.power(10.0, (dx, dy))
                start = np.array([p.x, p.y])
                oldpoints = p.lim.transformed(p.trans)
                newpoints = start + alpha * (oldpoints - start)
                result = (mtransforms.Bbox(newpoints)
                          .transformed(p.trans_inverse))
            except OverflowError:
                cbook._warn_external('Overflow while panning')
                return
        else:
            return

        valid = np.isfinite(result.transformed(p.trans))
        points = result.get_points().astype(object)
        # Just ignore invalid limits (typically, underflow in log-scale).
        points[~valid] = None
        self.set_xlim(points[:, 0])
        self.set_ylim(points[:, 1])
