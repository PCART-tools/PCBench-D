    def update(self, **kwargs):
        """
        Update the current values.  If any kwarg is None, default to
        the current value, if set, otherwise to rc.
        """

        for k, v in six.iteritems(kwargs):
            if k in self._AllowedKeys:
                setattr(self, k, v)
            else:
                raise AttributeError("%s is unknown keyword" % (k,))

        from matplotlib import _pylab_helpers
        from matplotlib.axes import SubplotBase
        for figmanager in six.itervalues(_pylab_helpers.Gcf.figs):
            for ax in figmanager.canvas.figure.axes:
                # copied from Figure.subplots_adjust
                if not isinstance(ax, SubplotBase):
                    # Check if sharing a subplots axis
                    if isinstance(ax._sharex, SubplotBase):
                        if ax._sharex.get_subplotspec().get_gridspec() == self:
                            ax._sharex.update_params()
                            ax.set_position(ax._sharex.figbox)
                    elif isinstance(ax._sharey, SubplotBase):
                        if ax._sharey.get_subplotspec().get_gridspec() == self:
                            ax._sharey.update_params()
                            ax.set_position(ax._sharey.figbox)
                else:
                    ss = ax.get_subplotspec().get_topmost_subplotspec()
                    if ss.get_gridspec() == self:
                        ax.update_params()
                        ax.set_position(ax.figbox)
