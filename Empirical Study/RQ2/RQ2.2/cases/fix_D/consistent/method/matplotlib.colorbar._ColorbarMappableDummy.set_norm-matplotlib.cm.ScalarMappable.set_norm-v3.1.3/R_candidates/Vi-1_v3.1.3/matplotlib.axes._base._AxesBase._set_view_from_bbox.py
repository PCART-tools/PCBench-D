    def _set_view_from_bbox(self, bbox, direction='in',
                            mode=None, twinx=False, twiny=False):
        """
        Update view from a selection bbox.

        .. note::

            Intended to be overridden by new projection types, but if not, the
            default implementation sets the view limits to the bbox directly.

        Parameters
        ----------

        bbox : 4-tuple or 3 tuple
            * If bbox is a 4 tuple, it is the selected bounding box limits,
                in *display* coordinates.
            * If bbox is a 3 tuple, it is an (xp, yp, scl) triple, where
                (xp,yp) is the center of zooming and scl the scale factor to
                zoom by.

        direction : str
            The direction to apply the bounding box.
                * `'in'` - The bounding box describes the view directly, i.e.,
                           it zooms in.
                * `'out'` - The bounding box describes the size to make the
                            existing view, i.e., it zooms out.

        mode : str or None
            The selection mode, whether to apply the bounding box in only the
            `'x'` direction, `'y'` direction or both (`None`).

        twinx : bool
            Whether this axis is twinned in the *x*-direction.

        twiny : bool
            Whether this axis is twinned in the *y*-direction.
        """
        Xmin, Xmax = self.get_xlim()
        Ymin, Ymax = self.get_ylim()

        if len(bbox) == 3:
            # Zooming code
            xp, yp, scl = bbox

            # Should not happen
            if scl == 0:
                scl = 1.

            # direction = 'in'
            if scl > 1:
                direction = 'in'
            else:
                direction = 'out'
                scl = 1/scl

            # get the limits of the axes
            tranD2C = self.transData.transform
            xmin, ymin = tranD2C((Xmin, Ymin))
            xmax, ymax = tranD2C((Xmax, Ymax))

            # set the range
            xwidth = xmax - xmin
            ywidth = ymax - ymin
            xcen = (xmax + xmin)*.5
            ycen = (ymax + ymin)*.5
            xzc = (xp*(scl - 1) + xcen)/scl
            yzc = (yp*(scl - 1) + ycen)/scl

            bbox = [xzc - xwidth/2./scl, yzc - ywidth/2./scl,
                    xzc + xwidth/2./scl, yzc + ywidth/2./scl]
        elif len(bbox) != 4:
            # should be len 3 or 4 but nothing else
            cbook._warn_external(
                "Warning in _set_view_from_bbox: bounding box is not a tuple "
                "of length 3 or 4. Ignoring the view change.")
            return

        # Just grab bounding box
        lastx, lasty, x, y = bbox

        # zoom to rect
        inverse = self.transData.inverted()
        lastx, lasty = inverse.transform_point((lastx, lasty))
        x, y = inverse.transform_point((x, y))

        if twinx:
            x0, x1 = Xmin, Xmax
        else:
            if Xmin < Xmax:
                if x < lastx:
                    x0, x1 = x, lastx
                else:
                    x0, x1 = lastx, x
                if x0 < Xmin:
                    x0 = Xmin
                if x1 > Xmax:
                    x1 = Xmax
            else:
                if x > lastx:
                    x0, x1 = x, lastx
                else:
                    x0, x1 = lastx, x
                if x0 > Xmin:
                    x0 = Xmin
                if x1 < Xmax:
                    x1 = Xmax

        if twiny:
            y0, y1 = Ymin, Ymax
        else:
            if Ymin < Ymax:
                if y < lasty:
                    y0, y1 = y, lasty
                else:
                    y0, y1 = lasty, y
                if y0 < Ymin:
                    y0 = Ymin
                if y1 > Ymax:
                    y1 = Ymax
            else:
                if y > lasty:
                    y0, y1 = y, lasty
                else:
                    y0, y1 = lasty, y
                if y0 > Ymin:
                    y0 = Ymin
                if y1 < Ymax:
                    y1 = Ymax

        if direction == 'in':
            if mode == 'x':
                self.set_xlim((x0, x1))
            elif mode == 'y':
                self.set_ylim((y0, y1))
            else:
                self.set_xlim((x0, x1))
                self.set_ylim((y0, y1))
        elif direction == 'out':
            if self.get_xscale() == 'log':
                alpha = np.log(Xmax / Xmin) / np.log(x1 / x0)
                rx1 = pow(Xmin / x0, alpha) * Xmin
                rx2 = pow(Xmax / x0, alpha) * Xmin
            else:
                alpha = (Xmax - Xmin) / (x1 - x0)
                rx1 = alpha * (Xmin - x0) + Xmin
                rx2 = alpha * (Xmax - x0) + Xmin
            if self.get_yscale() == 'log':
                alpha = np.log(Ymax / Ymin) / np.log(y1 / y0)
                ry1 = pow(Ymin / y0, alpha) * Ymin
                ry2 = pow(Ymax / y0, alpha) * Ymin
            else:
                alpha = (Ymax - Ymin) / (y1 - y0)
                ry1 = alpha * (Ymin - y0) + Ymin
                ry2 = alpha * (Ymax - y0) + Ymin

            if mode == 'x':
                self.set_xlim((rx1, rx2))
            elif mode == 'y':
                self.set_ylim((ry1, ry2))
            else:
                self.set_xlim((rx1, rx2))
                self.set_ylim((ry1, ry2))
