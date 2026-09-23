    def as_unit(self: _TDT, unit: str) -> _TDT:
        """
        Convert to a dtype with the given unit resolution.

        Parameters
        ----------
        unit : {'s', 'ms', 'us', 'ns'}

        Returns
        -------
        same type as self
        """
        arr = self._data.as_unit(unit)
        return type(self)._simple_new(arr, name=self.name)
