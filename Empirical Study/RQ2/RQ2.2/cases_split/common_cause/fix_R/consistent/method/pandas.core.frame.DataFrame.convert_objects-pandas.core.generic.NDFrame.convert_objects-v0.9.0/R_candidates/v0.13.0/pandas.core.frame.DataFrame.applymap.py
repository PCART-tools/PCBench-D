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

        See also
        --------
        DataFrame.apply : For operations on rows/columns

        """

        # if we have a dtype == 'M8[ns]', provide boxed values
        def infer(x):
            if com.is_datetime64_dtype(x):
                x = lib.map_infer(_values_from_object(x), lib.Timestamp)
            return lib.map_infer(_values_from_object(x), func)
        return self.apply(infer)
