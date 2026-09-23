    def _prepare_view_from_bbox(self, bbox, direction='in',
                                mode=None, twinx=False, twiny=False):
        """
        Helper function to prepare the new bounds from a bbox.

        This helper function returns the new x and y bounds from the zoom
        bbox. This a convenience method to abstract the bbox logic
        out of the base setter.
        """
        if len(bbox) == 3:
            xp, yp, scl = bbox  # Zooming code
            if scl == 0:  # Should not happen
                scl = 1.
            if scl > 1:
                direction = 'in'
            else:
                direction = 'out'
                scl = 1/scl
            # get the limits of the axes
            (xmin, ymin), (xmax, ymax) = self.transData.transform(
                np.transpose([self.get_xlim(), self.get_ylim()]))
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
            _api.warn_external(
                "Warning in _set_view_from_bbox: bounding box is not a tuple "
                "of length 3 or 4. Ignoring the view change.")
            return

        # Original limits.
        xmin0, xmax0 = self.get_xbound()
        ymin0, ymax0 = self.get_ybound()
        # The zoom box in screen coords.
        startx, starty, stopx, stopy = bbox
        # Convert to data coords.
        (startx, starty), (stopx, stopy) = self.transData.inverted().transform(
            [(startx, starty), (stopx, stopy)])
        # Clip to axes limits.
        xmin, xmax = np.clip(sorted([startx, stopx]), xmin0, xmax0)
        ymin, ymax = np.clip(sorted([starty, stopy]), ymin0, ymax0)
        # Don't double-zoom twinned axes or if zooming only the other axis.
        if twinx or mode == "y":
            xmin, xmax = xmin0, xmax0
        if twiny or mode == "x":
            ymin, ymax = ymin0, ymax0

        if direction == "in":
            new_xbound = xmin, xmax
            new_ybound = ymin, ymax

        elif direction == "out":
            x_trf = self.xaxis.get_transform()
            sxmin0, sxmax0, sxmin, sxmax = x_trf.transform(
                [xmin0, xmax0, xmin, xmax])  # To screen space.
            factor = (sxmax0 - sxmin0) / (sxmax - sxmin)  # Unzoom factor.
            # Move original bounds away by
            # (factor) x (distance between unzoom box and Axes bbox).
            sxmin1 = sxmin0 - factor * (sxmin - sxmin0)
            sxmax1 = sxmax0 + factor * (sxmax0 - sxmax)
            # And back to data space.
            new_xbound = x_trf.inverted().transform([sxmin1, sxmax1])

            y_trf = self.yaxis.get_transform()
            symin0, symax0, symin, symax = y_trf.transform(
                [ymin0, ymax0, ymin, ymax])
            factor = (symax0 - symin0) / (symax - symin)
            symin1 = symin0 - factor * (symin - symin0)
            symax1 = symax0 + factor * (symax0 - symax)
            new_ybound = y_trf.inverted().transform([symin1, symax1])

        return new_xbound, new_ybound
