    def get_subplotspec(self):
        # make tight_layout happy..
        ss = getattr(self._cbar.ax, 'get_subplotspec', None)
        if ss is None:
            ss = self._orig_locator.get_subplotspec()
        else:
            ss = ss()
        return ss
