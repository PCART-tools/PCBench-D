    def to_dask_dataframe(self, columns=None):
        """ Convert dask Array to dask Dataframe

        Parameters
        ----------
        columns: list or string
            list of column names if DataFrame, single string if Series

        See Also
        --------
        dask.dataframe.from_dask_array
        """
        from ..dataframe import from_dask_array
        return from_dask_array(self, columns=columns)
