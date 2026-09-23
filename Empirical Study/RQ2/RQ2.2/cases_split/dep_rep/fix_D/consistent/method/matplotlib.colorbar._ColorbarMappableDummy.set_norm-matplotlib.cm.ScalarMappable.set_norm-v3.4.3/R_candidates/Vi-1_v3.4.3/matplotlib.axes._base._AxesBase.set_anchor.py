    def set_anchor(self, anchor, share=False):
        """
        Define the anchor location.

        The actual drawing area (active position) of the Axes may be smaller
        than the Bbox (original position) when a fixed aspect is required. The
        anchor defines where the drawing area will be located within the
        available space.

        Parameters
        ----------
        anchor : 2-tuple of floats or {'C', 'SW', 'S', 'SE', ...}
            The anchor position may be either:

            - a sequence (*cx*, *cy*). *cx* and *cy* may range from 0
              to 1, where 0 is left or bottom and 1 is right or top.

            - a string using cardinal directions as abbreviation:

              - 'C' for centered
              - 'S' (south) for bottom-center
              - 'SW' (south west) for bottom-left
              - etc.

              Here is an overview of the possible positions:

              +------+------+------+
              | 'NW' | 'N'  | 'NE' |
              +------+------+------+
              | 'W'  | 'C'  | 'E'  |
              +------+------+------+
              | 'SW' | 'S'  | 'SE' |
              +------+------+------+

        share : bool, default: False
            If ``True``, apply the settings to all shared Axes.

        See Also
        --------
        matplotlib.axes.Axes.set_aspect
            for a description of aspect handling.
        """
        if not (anchor in mtransforms.Bbox.coefs or len(anchor) == 2):
            raise ValueError('argument must be among %s' %
                             ', '.join(mtransforms.Bbox.coefs))
        if share:
            axes = {*self._shared_x_axes.get_siblings(self),
                    *self._shared_y_axes.get_siblings(self)}
        else:
            axes = [self]
        for ax in axes:
            ax._anchor = anchor

        self.stale = True
