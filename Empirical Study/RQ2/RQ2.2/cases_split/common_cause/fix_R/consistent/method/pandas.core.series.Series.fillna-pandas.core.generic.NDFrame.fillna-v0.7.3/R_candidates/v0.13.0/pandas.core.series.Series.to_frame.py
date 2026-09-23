    def to_frame(self, name=None):
        """
        Convert Series to DataFrame

        Parameters
        ----------
        name : object, default None
            The passed name should substitute for the series name (if it has
            one).

        Returns
        -------
        data_frame : DataFrame
        """
        from pandas.core.frame import DataFrame
        if name is None:
            df = DataFrame(self)
        else:
            df = DataFrame({name: self})

        return df
