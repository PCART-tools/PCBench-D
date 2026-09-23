    def groupby(self, function, axis='major'):
        """
        Group data on given axis, returning GroupBy object

        Parameters
        ----------
        function : callable
            Mapping function for chosen access
        axis : {'major', 'minor', 'items'}, default 'major'

        Returns
        -------
        grouped : PanelGroupBy
        """
        from pandas.core.groupby.groupby import PanelGroupBy
        axis = self._get_axis_number(axis)
        return PanelGroupBy(self, function, axis=axis)
