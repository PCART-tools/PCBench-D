    def _unpickle_panel_compat(self, state):  # pragma: no cover
        "Unpickle the panel"
        from pandas.io.pickle import _unpickle_array

        _unpickle = _unpickle_array
        vals, items, major, minor = state

        items = _unpickle(items)
        major = _unpickle(major)
        minor = _unpickle(minor)
        values = _unpickle(vals)
        wp = Panel(values, items, major, minor)
        self._data = wp._data
