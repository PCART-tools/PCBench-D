    def __init__(self, ax, mappable, **kw):
        # Ensure the given mappable's norm has appropriate vmin and vmax set
        # even if mappable.draw has not yet been called.
        if mappable.get_array() is not None:
            mappable.autoscale_None()

        self.mappable = mappable
        kw['cmap'] = cmap = mappable.cmap
        kw['norm'] = mappable.norm

        if isinstance(mappable, contour.ContourSet):
            CS = mappable
            kw['alpha'] = mappable.get_alpha()
            kw['boundaries'] = CS._levels
            kw['values'] = CS.cvalues
            kw['extend'] = CS.extend
            kw.setdefault('ticks', ticker.FixedLocator(CS.levels, nbins=10))
            kw['filled'] = CS.filled
            ColorbarBase.__init__(self, ax, **kw)
            if not CS.filled:
                self.add_lines(CS)
        else:
            if getattr(cmap, 'colorbar_extend', False) is not False:
                kw.setdefault('extend', cmap.colorbar_extend)

            if isinstance(mappable, martist.Artist):
                kw['alpha'] = mappable.get_alpha()

            ColorbarBase.__init__(self, ax, **kw)
