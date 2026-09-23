    def applymap(self, func):
        """
        Apply a function to a DataFrame that is intended to operate
        elementwise, i.e. like doing map(func, series) for each series in the
        DataFrame

        Parameters
        ----------
        func : function
            Python function, returns a single value from a single value

        Returns
        -------
        applied : DataFrame
        """
        return self.apply(lambda x: lmap(func, x))
