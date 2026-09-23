    def _set_position(self, pos, which='both'):
        """
        Private version of set_position.

        Call this internally to get the same functionality of `set_position`,
        but not to take the axis out of the constrained_layout hierarchy.
        """
        if not isinstance(pos, mtransforms.BboxBase):
            pos = mtransforms.Bbox.from_bounds(*pos)
        for ax in self._twinned_axes.get_siblings(self):
            if which in ('both', 'active'):
                ax._position.set(pos)
            if which in ('both', 'original'):
                ax._originalPosition.set(pos)
        self.stale = True
