    def _check_layout_engines_compat(self, old, new):
        """
        Helper for set_layout engine

        If the figure has used the old engine and added a colorbar then the
        value of colorbar_gridspec must be the same on the new engine.
        """
        if old is None or new is None:
            return True
        if old.colorbar_gridspec == new.colorbar_gridspec:
            return True
        # colorbar layout different, so check if any colorbars are on the
        # figure...
        for ax in self.axes:
            if hasattr(ax, '_colorbar'):
                # colorbars list themselves as a colorbar.
                return False
        return True
