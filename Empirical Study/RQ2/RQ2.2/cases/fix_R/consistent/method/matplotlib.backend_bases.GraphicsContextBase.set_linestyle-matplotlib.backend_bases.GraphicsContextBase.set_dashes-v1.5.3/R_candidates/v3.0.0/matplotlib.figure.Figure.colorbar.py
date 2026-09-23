    @docstring.dedent_interpd
    def colorbar(self, mappable, cax=None, ax=None, use_gridspec=True, **kw):
        """
        Create a colorbar for a ScalarMappable instance, *mappable*.

        Documentation for the pyplot thin wrapper:
        %(colorbar_doc)s
        """
        if ax is None:
            ax = self.gca()

        # Store the value of gca so that we can set it back later on.
        current_ax = self.gca()

        if cax is None:
            if use_gridspec and isinstance(ax, SubplotBase)  \
                     and (not self.get_constrained_layout()):
                cax, kw = cbar.make_axes_gridspec(ax, **kw)
            else:
                cax, kw = cbar.make_axes(ax, **kw)

        # need to remove kws that cannot be passed to Colorbar
        NON_COLORBAR_KEYS = ['fraction', 'pad', 'shrink', 'aspect', 'anchor',
                             'panchor']
        cb_kw = {k: v for k, v in kw.items() if k not in NON_COLORBAR_KEYS}
        cb = cbar.colorbar_factory(cax, mappable, **cb_kw)

        self.sca(current_ax)
        self.stale = True
        return cb
