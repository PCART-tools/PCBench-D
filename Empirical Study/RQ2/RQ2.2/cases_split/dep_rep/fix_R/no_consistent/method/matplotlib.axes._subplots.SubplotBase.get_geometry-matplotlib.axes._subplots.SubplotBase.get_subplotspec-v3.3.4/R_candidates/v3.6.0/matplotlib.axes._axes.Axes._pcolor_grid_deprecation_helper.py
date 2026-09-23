    def _pcolor_grid_deprecation_helper(self):
        grid_active = any(axis._major_tick_kw["gridOn"]
                          for axis in self._axis_map.values())
        # explicit is-True check because get_axisbelow() can also be 'line'
        grid_hidden_by_pcolor = self.get_axisbelow() is True
        if grid_active and not grid_hidden_by_pcolor:
            _api.warn_deprecated(
                "3.5", message="Auto-removal of grids by pcolor() and "
                "pcolormesh() is deprecated since %(since)s and will be "
                "removed %(removal)s; please call grid(False) first.")
        self.grid(False)
