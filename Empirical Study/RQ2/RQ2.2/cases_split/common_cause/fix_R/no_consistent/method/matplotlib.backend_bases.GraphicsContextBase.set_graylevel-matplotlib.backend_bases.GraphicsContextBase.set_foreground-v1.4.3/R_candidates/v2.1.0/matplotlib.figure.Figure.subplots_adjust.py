    def subplots_adjust(self, *args, **kwargs):
        """
        Call signature::

          subplots_adjust(left=None, bottom=None, right=None, top=None,
                              wspace=None, hspace=None)

        Update the :class:`SubplotParams` with *kwargs* (defaulting to rc when
        *None*) and update the subplot locations

        """
        self.subplotpars.update(*args, **kwargs)
        for ax in self.axes:
            if not isinstance(ax, SubplotBase):
                # Check if sharing a subplots axis
                if isinstance(ax._sharex, SubplotBase):
                    ax._sharex.update_params()
                    ax.set_position(ax._sharex.figbox)
                elif isinstance(ax._sharey, SubplotBase):
                    ax._sharey.update_params()
                    ax.set_position(ax._sharey.figbox)
            else:
                ax.update_params()
                ax.set_position(ax.figbox)
        self.stale = True
