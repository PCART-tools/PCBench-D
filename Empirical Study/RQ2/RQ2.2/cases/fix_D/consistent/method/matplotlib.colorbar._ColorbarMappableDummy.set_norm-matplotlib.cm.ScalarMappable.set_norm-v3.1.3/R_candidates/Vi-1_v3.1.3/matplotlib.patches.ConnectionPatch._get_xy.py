    def _get_xy(self, x, y, s, axes=None):
        """
        calculate the pixel position of given point
        """

        if axes is None:
            axes = self.axes

        if s == 'data':
            trans = axes.transData
            x = float(self.convert_xunits(x))
            y = float(self.convert_yunits(y))
            return trans.transform_point((x, y))
        elif s == 'offset points':
            # convert the data point
            dx, dy = self.xy

            # prevent recursion
            if self.xycoords == 'offset points':
                return self._get_xy(dx, dy, 'data')

            dx, dy = self._get_xy(dx, dy, self.xycoords)

            # convert the offset
            dpi = self.figure.get_dpi()
            x *= dpi / 72.
            y *= dpi / 72.

            # add the offset to the data point
            x += dx
            y += dy

            return x, y
        elif s == 'polar':
            theta, r = x, y
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            trans = axes.transData
            return trans.transform_point((x, y))
        elif s == 'figure points':
            # points from the lower left corner of the figure
            dpi = self.figure.dpi
            l, b, w, h = self.figure.bbox.bounds
            r = l + w
            t = b + h

            x *= dpi / 72.
            y *= dpi / 72.
            if x < 0:
                x = r + x
            if y < 0:
                y = t + y
            return x, y
        elif s == 'figure pixels':
            # pixels from the lower left corner of the figure
            l, b, w, h = self.figure.bbox.bounds
            r = l + w
            t = b + h
            if x < 0:
                x = r + x
            if y < 0:
                y = t + y
            return x, y
        elif s == 'figure fraction':
            # (0,0) is lower left, (1,1) is upper right of figure
            trans = self.figure.transFigure
            return trans.transform_point((x, y))
        elif s == 'axes points':
            # points from the lower left corner of the axes
            dpi = self.figure.dpi
            l, b, w, h = axes.bbox.bounds
            r = l + w
            t = b + h
            if x < 0:
                x = r + x * dpi / 72.
            else:
                x = l + x * dpi / 72.
            if y < 0:
                y = t + y * dpi / 72.
            else:
                y = b + y * dpi / 72.
            return x, y
        elif s == 'axes pixels':
            #pixels from the lower left corner of the axes

            l, b, w, h = axes.bbox.bounds
            r = l + w
            t = b + h
            if x < 0:
                x = r + x
            else:
                x = l + x
            if y < 0:
                y = t + y
            else:
                y = b + y
            return x, y
        elif s == 'axes fraction':
            #(0,0) is lower left, (1,1) is upper right of axes
            trans = axes.transAxes
            return trans.transform_point((x, y))
        elif isinstance(s, transforms.Transform):
            return s.transform_point((x, y))
        else:
            raise ValueError("{} is not a valid coordinate "
                             "transformation.".format(s))
