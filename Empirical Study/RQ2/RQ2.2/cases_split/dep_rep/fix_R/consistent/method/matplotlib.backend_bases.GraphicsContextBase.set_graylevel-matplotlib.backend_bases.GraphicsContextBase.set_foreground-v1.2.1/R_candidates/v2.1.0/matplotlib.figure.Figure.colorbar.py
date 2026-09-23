    @docstring.dedent_interpd
    def colorbar(self, mappable, cax=None, ax=None, use_gridspec=True, **kw):
        """
        Create a colorbar for a ScalarMappable instance, *mappable*.

        Documentation for the pylab thin wrapper:
        %(colorbar_doc)s
        """
        if ax is None:
            ax = self.gca()

        # Store the value of gca so that we can set it back later on.
        current_ax = self.gca()

        if cax is None:
            if use_gridspec and isinstance(ax, SubplotBase):
                cax, kw = cbar.make_axes_gridspec(ax, **kw)
            else:
                cax, kw = cbar.make_axes(ax, **kw)
        cax._hold = True
        cb = cbar.colorbar_factory(cax, mappable, **kw)

        self.sca(current_ax)
        self.stale = True
        return cb
