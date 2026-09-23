    def locate_label(self, linecontour, labelwidth):
        """
        Find good place to draw a label (relatively flat part of the contour).
        """

        # Number of contour points
        nsize = len(linecontour)
        if labelwidth > 1:
            xsize = int(np.ceil(nsize / labelwidth))
        else:
            xsize = 1
        if xsize == 1:
            ysize = nsize
        else:
            ysize = int(labelwidth)

        XX = np.resize(linecontour[:, 0], (xsize, ysize))
        YY = np.resize(linecontour[:, 1], (xsize, ysize))
        # I might have fouled up the following:
        yfirst = YY[:, :1]
        ylast = YY[:, -1:]
        xfirst = XX[:, :1]
        xlast = XX[:, -1:]
        s = (yfirst - YY) * (xlast - xfirst) - (xfirst - XX) * (ylast - yfirst)
        L = np.hypot(xlast - xfirst, ylast - yfirst)
        # Ignore warning that divide by zero throws, as this is a valid option
        with np.errstate(divide='ignore', invalid='ignore'):
            dist = np.sum(np.abs(s) / L, axis=-1)
        x, y, ind = self.get_label_coords(dist, XX, YY, ysize, labelwidth)

        # There must be a more efficient way...
        lc = [tuple(l) for l in linecontour]
        dind = lc.index((x, y))

        return x, y, dind
