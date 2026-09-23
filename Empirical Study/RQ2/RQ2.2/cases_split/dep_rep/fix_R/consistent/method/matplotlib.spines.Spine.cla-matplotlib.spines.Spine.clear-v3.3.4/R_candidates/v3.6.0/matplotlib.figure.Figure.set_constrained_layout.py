    @_api.deprecated("3.6", alternative="set_layout_engine('constrained')",
                     pending=True)
    def set_constrained_layout(self, constrained):
        """
        [*Discouraged*] Set whether ``constrained_layout`` is used upon
        drawing.

        If None, :rc:`figure.constrained_layout.use` value will be used.

        When providing a dict containing the keys ``w_pad``, ``h_pad``
        the default ``constrained_layout`` paddings will be
        overridden.  These pads are in inches and default to 3.0/72.0.
        ``w_pad`` is the width padding and ``h_pad`` is the height padding.

        .. admonition:: Discouraged

            This method is discouraged in favor of `~.set_layout_engine`.

        Parameters
        ----------
        constrained : bool or dict or None
        """
        if constrained is None:
            constrained = mpl.rcParams['figure.constrained_layout.use']
        _constrained = bool(constrained)
        _parameters = constrained if isinstance(constrained, dict) else {}
        if _constrained:
            self.set_layout_engine(ConstrainedLayoutEngine(**_parameters))
        self.stale = True
