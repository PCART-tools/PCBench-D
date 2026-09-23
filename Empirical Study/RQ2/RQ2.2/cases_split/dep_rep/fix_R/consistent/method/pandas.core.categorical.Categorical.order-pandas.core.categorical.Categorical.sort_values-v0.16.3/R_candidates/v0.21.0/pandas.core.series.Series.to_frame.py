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
        if name is None:
            df = self._constructor_expanddim(self)
        else:
            df = self._constructor_expanddim({name: self})

        return df
