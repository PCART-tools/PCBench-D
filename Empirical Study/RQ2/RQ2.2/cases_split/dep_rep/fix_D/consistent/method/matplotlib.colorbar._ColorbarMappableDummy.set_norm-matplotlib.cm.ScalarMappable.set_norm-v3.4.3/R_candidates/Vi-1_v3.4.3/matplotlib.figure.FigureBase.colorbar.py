    @docstring.dedent_interpd
    def colorbar(self, mappable, cax=None, ax=None, use_gridspec=True, **kw):
        """%(colorbar_doc)s"""
        if ax is None:
            ax = self.gca()
            if (hasattr(mappable, "axes") and ax is not mappable.axes
                    and cax is None):
                _api.warn_deprecated(
                    "3.4", message="Starting from Matplotlib 3.6, colorbar() "
                    "will steal space from the mappable's axes, rather than "
                    "from the current axes, to place the colorbar.  To "
                    "silence this warning, explicitly pass the 'ax' argument "
                    "to colorbar().")

        # Store the value of gca so that we can set it back later on.
        current_ax = self.gca()
        if cax is None:
            if (use_gridspec and isinstance(ax, SubplotBase)
                    and not self.get_constrained_layout()):
                cax, kw = cbar.make_axes_gridspec(ax, **kw)
            else:
                cax, kw = cbar.make_axes(ax, **kw)

        # need to remove kws that cannot be passed to Colorbar
        NON_COLORBAR_KEYS = ['fraction', 'pad', 'shrink', 'aspect', 'anchor',
                             'panchor']
        cb_kw = {k: v for k, v in kw.items() if k not in NON_COLORBAR_KEYS}
        cb = cbar.Colorbar(cax, mappable, **cb_kw)

        self.sca(current_ax)
        self.stale = True
        return cb
