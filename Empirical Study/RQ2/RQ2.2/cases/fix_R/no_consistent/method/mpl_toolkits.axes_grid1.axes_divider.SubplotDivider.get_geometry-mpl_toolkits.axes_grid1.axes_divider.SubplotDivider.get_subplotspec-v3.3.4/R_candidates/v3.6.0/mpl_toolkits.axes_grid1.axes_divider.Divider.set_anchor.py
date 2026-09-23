    def set_anchor(self, anchor):
        """
        Parameters
        ----------
        anchor : (float, float) or {'C', 'SW', 'S', 'SE', 'E', 'NE', 'N', \
'NW', 'W'}
            Either an (*x*, *y*) pair of relative coordinates (0 is left or
            bottom, 1 is right or top), 'C' (center), or a cardinal direction
            ('SW', southwest, is bottom left, etc.).

        See Also
        --------
        .Axes.set_anchor
        """
        if isinstance(anchor, str):
            _api.check_in_list(mtransforms.Bbox.coefs, anchor=anchor)
        elif not isinstance(anchor, (tuple, list)) or len(anchor) != 2:
            raise TypeError("anchor must be str or 2-tuple")
        self._anchor = anchor
