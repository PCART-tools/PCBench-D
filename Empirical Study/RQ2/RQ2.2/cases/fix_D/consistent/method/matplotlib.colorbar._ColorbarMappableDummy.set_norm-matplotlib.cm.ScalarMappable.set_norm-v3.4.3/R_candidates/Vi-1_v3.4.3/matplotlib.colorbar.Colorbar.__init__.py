    def __init__(self, ax, mappable, **kwargs):
        # Ensure the given mappable's norm has appropriate vmin and vmax set
        # even if mappable.draw has not yet been called.
        if mappable.get_array() is not None:
            mappable.autoscale_None()

        self.mappable = mappable
        _add_disjoint_kwargs(kwargs, cmap=mappable.cmap, norm=mappable.norm)

        if isinstance(mappable, contour.ContourSet):
            cs = mappable
            _add_disjoint_kwargs(
                kwargs,
                alpha=cs.get_alpha(),
                boundaries=cs._levels,
                values=cs.cvalues,
                extend=cs.extend,
                filled=cs.filled,
            )
            kwargs.setdefault(
                'ticks', ticker.FixedLocator(cs.levels, nbins=10))
            super().__init__(ax, **kwargs)
            if not cs.filled:
                self.add_lines(cs)
        else:
            if getattr(mappable.cmap, 'colorbar_extend', False) is not False:
                kwargs.setdefault('extend', mappable.cmap.colorbar_extend)
            if isinstance(mappable, martist.Artist):
                _add_disjoint_kwargs(kwargs, alpha=mappable.get_alpha())
            super().__init__(ax, **kwargs)

        mappable.colorbar = self
        mappable.colorbar_cid = mappable.callbacksSM.connect(
            'changed', self.update_normal)
