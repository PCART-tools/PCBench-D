class StrCategoryLocator(ticker.Locator):
    """Tick at every integer mapping of the string data."""
    def __init__(self, units_mapping):
        """
        Parameters
        ----------
        units_mapping : dict
            Mapping of category names (str) to indices (int).
        """
        self._units = units_mapping

    def __call__(self):
        # docstring inherited
        return list(self._units.values())

    def tick_values(self, vmin, vmax):
        # docstring inherited
        return self()
