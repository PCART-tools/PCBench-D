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
        name = '{0}_{1}_{2}'.format(type(value).__name__, self.ntemps,
                                    _raw_hex_id(self))

        # add to inner most scope
        assert name not in self.temps
        self.temps[name] = value
        assert name in self.temps

        # only increment if the variable gets put in the scope
        return name
