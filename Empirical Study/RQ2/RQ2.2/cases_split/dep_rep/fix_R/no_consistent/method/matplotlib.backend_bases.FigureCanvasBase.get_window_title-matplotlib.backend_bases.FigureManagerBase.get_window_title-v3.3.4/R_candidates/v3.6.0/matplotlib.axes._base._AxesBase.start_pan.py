    def start_pan(self, x, y, button):
        """
        Called when a pan operation has started.

        Parameters
        ----------
        x, y : float
            The mouse coordinates in display coords.
        button : `.MouseButton`
            The pressed mouse button.

        Notes
        -----
        This is intended to be overridden by new projection types.
        """
        self._pan_start = types.SimpleNamespace(
            lim=self.viewLim.frozen(),
            trans=self.transData.frozen(),
            trans_inverse=self.transData.inverted().frozen(),
            bbox=self.bbox.frozen(),
            x=x,
            y=y)
