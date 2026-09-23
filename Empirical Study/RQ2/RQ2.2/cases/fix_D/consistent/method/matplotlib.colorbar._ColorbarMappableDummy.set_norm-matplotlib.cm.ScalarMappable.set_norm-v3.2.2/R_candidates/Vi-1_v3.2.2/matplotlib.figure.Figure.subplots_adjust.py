    def subplots_adjust(self, left=None, bottom=None, right=None, top=None,
                        wspace=None, hspace=None):
        """
        Update the :class:`SubplotParams` with *kwargs* (defaulting to rc when
        *None*) and update the subplot locations.

        """
        if self.get_constrained_layout():
            self.set_constrained_layout(False)
            cbook._warn_external("This figure was using "
                                 "constrained_layout==True, but that is "
                                 "incompatible with subplots_adjust and or "
                                 "tight_layout: setting "
                                 "constrained_layout==False. ")
        self.subplotpars.update(left, bottom, right, top, wspace, hspace)
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
