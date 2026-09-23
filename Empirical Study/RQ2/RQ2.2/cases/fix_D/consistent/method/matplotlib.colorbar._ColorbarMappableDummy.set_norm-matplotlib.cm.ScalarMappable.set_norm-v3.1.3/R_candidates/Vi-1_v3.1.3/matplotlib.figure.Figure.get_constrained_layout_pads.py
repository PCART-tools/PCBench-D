    def get_constrained_layout_pads(self, relative=False):
        """
        Get padding for ``constrained_layout``.

        Returns a list of `w_pad, h_pad` in inches and
        `wspace` and `hspace` as fractions of the subplot.

        See :doc:`/tutorials/intermediate/constrainedlayout_guide`.

        Parameters
        ----------

        relative : boolean
            If `True`, then convert from inches to figure relative.
        """
        w_pad = self._constrained_layout_pads['w_pad']
        h_pad = self._constrained_layout_pads['h_pad']
        wspace = self._constrained_layout_pads['wspace']
        hspace = self._constrained_layout_pads['hspace']

        if relative and (w_pad is not None or h_pad is not None):
            renderer0 = layoutbox.get_renderer(self)
            dpi = renderer0.dpi
            w_pad = w_pad * dpi / renderer0.width
            h_pad = h_pad * dpi / renderer0.height

        return w_pad, h_pad, wspace, hspace
