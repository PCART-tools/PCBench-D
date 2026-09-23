    def _pcolor_grid_deprecation_helper(self):
        if any(axis._major_tick_kw["gridOn"]
               for axis in self._get_axis_list()):
            _api.warn_deprecated(
                "3.5", message="Auto-removal of grids by pcolor() and "
                "pcolormesh() is deprecated since %(since)s and will be "
                "removed %(removal)s; please call grid(False) first.")
        self.grid(False)
