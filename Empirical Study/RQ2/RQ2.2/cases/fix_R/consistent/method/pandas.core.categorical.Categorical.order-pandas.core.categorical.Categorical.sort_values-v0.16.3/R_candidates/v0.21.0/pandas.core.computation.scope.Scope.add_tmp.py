    def add_tmp(self, value):
        """Add a temporary variable to the scope.

        Parameters
        ----------
        value : object
            An arbitrary object to be assigned to a temporary variable.

        Returns
        -------
        name : basestring
            The name of the temporary variable created.
        """
        name = '{name}_{num}_{hex_id}'.format(name=type(value).__name__,
                                              num=self.ntemps,
                                              hex_id=_raw_hex_id(self))

        # add to inner most scope
        assert name not in self.temps
        self.temps[name] = value
        assert name in self.temps

        # only increment if the variable gets put in the scope
        return name
