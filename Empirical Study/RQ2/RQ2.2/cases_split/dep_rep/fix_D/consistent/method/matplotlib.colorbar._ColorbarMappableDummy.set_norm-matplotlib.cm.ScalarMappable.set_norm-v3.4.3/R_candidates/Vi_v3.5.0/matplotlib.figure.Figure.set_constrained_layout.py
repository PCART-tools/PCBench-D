    def set_constrained_layout(self, constrained):
        """
        Set whether ``constrained_layout`` is used upon drawing. If None,
        :rc:`figure.constrained_layout.use` value will be used.

        When providing a dict containing the keys `w_pad`, `h_pad`
        the default ``constrained_layout`` paddings will be
        overridden.  These pads are in inches and default to 3.0/72.0.
        ``w_pad`` is the width padding and ``h_pad`` is the height padding.

        See :doc:`/tutorials/intermediate/constrainedlayout_guide`.

        Parameters
        ----------
        constrained : bool or dict or None
        """
        self._constrained_layout_pads = dict()
        self._constrained_layout_pads['w_pad'] = None
        self._constrained_layout_pads['h_pad'] = None
        self._constrained_layout_pads['wspace'] = None
        self._constrained_layout_pads['hspace'] = None
        if constrained is None:
            constrained = mpl.rcParams['figure.constrained_layout.use']
        self._constrained = bool(constrained)
        if isinstance(constrained, dict):
            self.set_constrained_layout_pads(**constrained)
        else:
            self.set_constrained_layout_pads()
        self.stale = True
