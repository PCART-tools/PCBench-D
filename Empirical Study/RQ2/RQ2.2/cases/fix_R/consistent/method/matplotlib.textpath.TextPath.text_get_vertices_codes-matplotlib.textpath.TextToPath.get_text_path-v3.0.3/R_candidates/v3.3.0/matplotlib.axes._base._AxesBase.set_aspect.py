    def set_aspect(self, aspect, adjustable=None, anchor=None, share=False):
        """
        Set the aspect of the axis scaling, i.e. the ratio of y-unit to x-unit.

        Parameters
        ----------
        aspect : {'auto'} or num
            Possible values:

            ========   =================================================
            value      description
            ========   =================================================
            'auto'     automatic; fill the position rectangle with data.
            num        a circle will be stretched such that the height
                       is *num* times the width.  'equal' is a synonym
                       for ``aspect=1``, i.e. same scaling for x and y.
            ========   =================================================

        adjustable : None or {'box', 'datalim'}, optional
            If not ``None``, this defines which parameter will be adjusted to
            meet the required aspect. See `.set_adjustable` for further
            details.

        anchor : None or str or 2-tuple of float, optional
            If not ``None``, this defines where the Axes will be drawn if there
            is extra space due to aspect constraints. The most common way to
            to specify the anchor are abbreviations of cardinal directions:

            =====   =====================
            value   description
            =====   =====================
            'C'     centered
            'SW'    lower left corner
            'S'     middle of bottom edge
            'SE'    lower right corner
            etc.
            =====   =====================

            See `.set_anchor` for further details.

        share : bool, default: False
            If ``True``, apply the settings to all shared Axes.

        See Also
        --------
        matplotlib.axes.Axes.set_adjustable
            Set how the Axes adjusts to achieve the required aspect ratio.
        matplotlib.axes.Axes.set_anchor
            Set the position in case of extra space.
        """
        if cbook._str_equal(aspect, 'equal'):
            aspect = 1
        if not cbook._str_equal(aspect, 'auto'):
            aspect = float(aspect)  # raise ValueError if necessary

        if share:
            axes = {*self._shared_x_axes.get_siblings(self),
                    *self._shared_y_axes.get_siblings(self)}
        else:
            axes = [self]

        for ax in axes:
            ax._aspect = aspect

        if adjustable is None:
            adjustable = self._adjustable
        self.set_adjustable(adjustable, share=share)  # Handle sharing.

        if anchor is not None:
            self.set_anchor(anchor, share=share)
        self.stale = True
