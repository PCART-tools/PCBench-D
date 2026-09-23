    def _dots_per_unit(self, units):
        """
        Return a scale factor for converting from units to pixels
        """
        ax = self.ax
        if units in ('x', 'y', 'xy'):
            if units == 'x':
                dx0 = ax.viewLim.width
                dx1 = ax.bbox.width
            elif units == 'y':
                dx0 = ax.viewLim.height
                dx1 = ax.bbox.height
            else:  # 'xy' is assumed
                dxx0 = ax.viewLim.width
                dxx1 = ax.bbox.width
                dyy0 = ax.viewLim.height
                dyy1 = ax.bbox.height
                dx1 = np.hypot(dxx1, dyy1)
                dx0 = np.hypot(dxx0, dyy0)
            dx = dx1 / dx0
        else:
            if units == 'width':
                dx = ax.bbox.width
            elif units == 'height':
                dx = ax.bbox.height
            elif units == 'dots':
                dx = 1.0
            elif units == 'inches':
                dx = ax.figure.dpi
            else:
                raise ValueError('unrecognized units')
        return dx
