    def _dots_per_unit(self, units):
        """
        Return a scale factor for converting from units to pixels
        """
        if units in ('x', 'y', 'xy'):
            if units == 'x':
                dx0 = self.axes.viewLim.width
                dx1 = self.axes.bbox.width
            elif units == 'y':
                dx0 = self.axes.viewLim.height
                dx1 = self.axes.bbox.height
            else:  # 'xy' is assumed
                dxx0 = self.axes.viewLim.width
                dxx1 = self.axes.bbox.width
                dyy0 = self.axes.viewLim.height
                dyy1 = self.axes.bbox.height
                dx1 = np.hypot(dxx1, dyy1)
                dx0 = np.hypot(dxx0, dyy0)
            dx = dx1 / dx0
        else:
            if units == 'width':
                dx = self.axes.bbox.width
            elif units == 'height':
                dx = self.axes.bbox.height
            elif units == 'dots':
                dx = 1.0
            elif units == 'inches':
                dx = self.axes.figure.dpi
            else:
                raise ValueError('unrecognized units')
        return dx
