    def to_parquet(self, fname, engine='auto', compression='snappy',
                   **kwargs):
        """
        Write a DataFrame to the binary parquet format.

        .. versionadded:: 0.21.0

        Parameters
        ----------
        fname : str
            string file path
        engine : {'auto', 'pyarrow', 'fastparquet'}, default 'auto'
            Parquet reader library to use. If 'auto', then the option
            'io.parquet.engine' is used. If 'auto', then the first
            library to be installed is used.
        compression : str, optional, default 'snappy'
            compression method, includes {'gzip', 'snappy', 'brotli'}
        kwargs
            Additional keyword arguments passed to the engine
        """
        from pandas.io.parquet import to_parquet
        to_parquet(self, fname, engine,
                   compression=compression, **kwargs)
