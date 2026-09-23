    def set_constrained_layout_pads(self, **kwargs):
        """
        Set padding for ``constrained_layout``.  Note the kwargs can be passed
        as a dictionary ``fig.set_constrained_layout(**paddict)``.

        See :doc:`/tutorials/intermediate/constrainedlayout_guide`.

        Parameters
        ----------

        w_pad : scalar
            Width padding in inches.  This is the pad around axes
            and is meant to make sure there is enough room for fonts to
            look good.  Defaults to 3 pts = 0.04167 inches

        h_pad : scalar
            Height padding in inches. Defaults to 3 pts.

        wspace : scalar
            Width padding between subplots, expressed as a fraction of the
            subplot width.  The total padding ends up being w_pad + wspace.

        hspace : scalar
            Height padding between subplots, expressed as a fraction of the
            subplot width. The total padding ends up being h_pad + hspace.

        """

        todo = ['w_pad', 'h_pad', 'wspace', 'hspace']
        for td in todo:
            if td in kwargs and kwargs[td] is not None:
                self._constrained_layout_pads[td] = kwargs[td]
            else:
                self._constrained_layout_pads[td] = (
                    rcParams['figure.constrained_layout.' + td])
