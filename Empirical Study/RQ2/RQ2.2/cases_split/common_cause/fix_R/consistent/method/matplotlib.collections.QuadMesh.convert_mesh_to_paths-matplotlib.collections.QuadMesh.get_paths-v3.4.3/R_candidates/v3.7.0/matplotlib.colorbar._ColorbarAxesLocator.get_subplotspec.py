    def get_subplotspec(self):
        # make tight_layout happy..
        return (
            self._cbar.ax.get_subplotspec()
            or getattr(self._orig_locator, "get_subplotspec", lambda: None)())
