    def apply(self, func, axis='major'):
        """
        Apply

        Parameters
        ----------
        func : numpy function
            Signature should match numpy.{sum, mean, var, std} etc.
        axis : {'major', 'minor', 'items'}
        fill_value : boolean, default True
            Replace NaN values with specified first

        Returns
        -------
        result : DataFrame or Panel
        """
        i = self._get_axis_number(axis)
        result = np.apply_along_axis(func, i, self.values)
        return self._wrap_result(result, axis=axis)
