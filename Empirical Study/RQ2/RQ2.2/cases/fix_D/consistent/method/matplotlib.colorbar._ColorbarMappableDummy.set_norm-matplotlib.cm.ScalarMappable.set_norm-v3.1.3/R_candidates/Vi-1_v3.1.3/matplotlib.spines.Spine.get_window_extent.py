    def get_window_extent(self, renderer=None):
        """
        Return the window extent of the spines in display space, including
        padding for ticks (but not their labels)

        See Also
        --------
        matplotlib.axes.Axes.get_tightbbox
        matplotlib.axes.Axes.get_window_extent

        """
        # make sure the location is updated so that transforms etc are
        # correct:
        self._adjust_location()
        bb = super().get_window_extent(renderer=renderer)
        if self.axis is None:
            return bb
        bboxes = [bb]
        tickstocheck = [self.axis.majorTicks[0]]
        if len(self.axis.minorTicks) > 1:
            # only pad for minor ticks if there are more than one
            # of them.  There is always one...
            tickstocheck.append(self.axis.minorTicks[1])
        for tick in tickstocheck:
            bb0 = bb.frozen()
            tickl = tick._size
            tickdir = tick._tickdir
            if tickdir == 'out':
                padout = 1
                padin = 0
            elif tickdir == 'in':
                padout = 0
                padin = 1
            else:
                padout = 0.5
                padin = 0.5
            padout = padout * tickl / 72 * self.figure.dpi
            padin = padin * tickl / 72 * self.figure.dpi

            if tick.tick1line.get_visible():
                if self.spine_type in ['left']:
                    bb0.x0 = bb0.x0 - padout
                    bb0.x1 = bb0.x1 + padin
                elif self.spine_type in ['bottom']:
                    bb0.y0 = bb0.y0 - padout
                    bb0.y1 = bb0.y1 + padin

            if tick.tick2line.get_visible():
                if self.spine_type in ['right']:
                    bb0.x1 = bb0.x1 + padout
                    bb0.x0 = bb0.x0 - padin
                elif self.spine_type in ['top']:
                    bb0.y1 = bb0.y1 + padout
                    bb0.y0 = bb0.y0 - padout
            bboxes.append(bb0)

        return mtransforms.Bbox.union(bboxes)
