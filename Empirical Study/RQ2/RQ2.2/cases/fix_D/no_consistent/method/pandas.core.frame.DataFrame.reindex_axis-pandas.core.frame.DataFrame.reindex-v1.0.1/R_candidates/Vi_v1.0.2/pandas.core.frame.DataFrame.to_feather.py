    @deprecate_kwarg(old_arg_name="fname", new_arg_name="path")
    def to_feather(self, path) -> None:
        """
        Write out the binary feather-format for DataFrames.

        Parameters
        ----------
        path : str
            String file path.
        """
        from pandas.io.feather_format import to_feather

        to_feather(self, path)
