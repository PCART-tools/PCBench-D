    def _get_xy(self, xy, s, axes=None):
        """Calculate the pixel position of given point."""
        s0 = s  # For the error message, if needed.
        if axes is None:
            axes = self.axes

        # preserve mixed type input (such as str, int)
        x = np.array(xy[0])
        y = np.array(xy[1])

        fig = self.get_figure(root=False)
        if s in ["figure points", "axes points"]:
            x = x * fig.dpi / 72
            y = y * fig.dpi / 72
            s = s.replace("points", "pixels")
        elif s == "figure fraction":
            s = fig.transFigure
        elif s == "subfigure fraction":
            s = fig.transSubfigure
        elif s == "axes fraction":
            s = axes.transAxes

        if s == 'data':
            trans = axes.transData
            x = cbook._to_unmasked_float_array(axes.xaxis.convert_units(x))
            y = cbook._to_unmasked_float_array(axes.yaxis.convert_units(y))
            return trans.transform((x, y))
        elif s == 'offset points':
            if self.xycoords == 'offset points':  # prevent recursion
                return self._get_xy(self.xy, 'data')
            return (
                self._get_xy(self.xy, self.xycoords)  # converted data point
                + xy * self.get_figure(root=True).dpi / 72)  # converted offset
        elif s == 'polar':
            theta, r = x, y
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            trans = axes.transData
            return trans.transform((x, y))
        elif s == 'figure pixels':
            # pixels from the lower left corner of the figure
            bb = self.get_figure(root=False).figbbox
            x = bb.x0 + x if x >= 0 else bb.x1 + x
            y = bb.y0 + y if y >= 0 else bb.y1 + y
            return x, y
        elif s == 'subfigure pixels':
            # pixels from the lower left corner of the figure
            bb = self.get_figure(root=False).bbox
            x = bb.x0 + x if x >= 0 else bb.x1 + x
            y = bb.y0 + y if y >= 0 else bb.y1 + y
            return x, y
        elif s == 'axes pixels':
            # pixels from the lower left corner of the Axes
            bb = axes.bbox
            x = bb.x0 + x if x >= 0 else bb.x1 + x
            y = bb.y0 + y if y >= 0 else bb.y1 + y
            return x, y
        elif isinstance(s, transforms.Transform):
            return s.transform(xy)
        else:
            raise ValueError(f"{s0} is not a valid coordinate transformation")
