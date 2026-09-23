    def to_feather(self, fname):
        """
        Write out the binary feather-format for DataFrames.

        .. versionadded:: 0.20.0

        Parameters
        ----------
        fname : str
            string file path
        """
        from pandas.io.feather_format import to_feather

        to_feather(self, fname)
