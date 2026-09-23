    def update_normal(self, mappable=None):
        """
        Update solid patches, lines, etc.

        This is meant to be called when the norm of the image or contour plot
        to which this colorbar belongs changes.

        If the norm on the mappable is different than before, this resets the
        locator and formatter for the axis, so if these have been customized,
        they will need to be customized again.  However, if the norm only
        changes values of *vmin*, *vmax* or *cmap* then the old formatter
        and locator will be preserved.
        """
        if mappable:
            # The mappable keyword argument exists because
            # ScalarMappable.changed() emits self.callbacks.process('changed', self)
            # in contrast, ColorizingArtist (and Colorizer) does not use this keyword.
            # [ColorizingArtist.changed() emits self.callbacks.process('changed')]
            # Also, there is no test where self.mappable == mappable is not True
            # and possibly no use case.
            # Therefore, the mappable keyword can be deprecated if cm.ScalarMappable
            # is removed.
            self.mappable = mappable
        _log.debug('colorbar update normal %r %r', self.mappable.norm, self.norm)
        self.set_alpha(self.mappable.get_alpha())
        self.cmap = self.mappable.cmap
        if self.mappable.norm != self.norm:
            self.norm = self.mappable.norm
            self._reset_locator_formatter_scale()

        self._draw_all()
        if isinstance(self.mappable, contour.ContourSet):
            CS = self.mappable
            if not CS.filled:
                self.add_lines(CS)
        self.stale = True
