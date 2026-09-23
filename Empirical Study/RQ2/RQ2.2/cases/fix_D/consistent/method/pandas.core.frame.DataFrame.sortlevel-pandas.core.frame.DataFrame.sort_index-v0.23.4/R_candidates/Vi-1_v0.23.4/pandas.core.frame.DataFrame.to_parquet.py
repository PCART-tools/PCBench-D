    def to_parquet(self, fname, engine='auto', compression='snappy',
                   **kwargs):
        """
        Write a DataFrame to the binary parquet format.

        .. versionadded:: 0.21.0

        This function writes the dataframe as a `parquet file
        <https://parquet.apache.org/>`_. You can choose different parquet
        backends, and have the option of compression. See
        :ref:`the user guide <io.parquet>` for more details.

        Parameters
        ----------
        fname : str
            String file path.
        engine : {'auto', 'pyarrow', 'fastparquet'}, default 'auto'
            Parquet library to use. If 'auto', then the option
            ``io.parquet.engine`` is used. The default ``io.parquet.engine``
            behavior is to try 'pyarrow', falling back to 'fastparquet' if
            'pyarrow' is unavailable.
        compression : {'snappy', 'gzip', 'brotli', None}, default 'snappy'
            Name of the compression to use. Use ``None`` for no compression.
        **kwargs
            Additional arguments passed to the parquet library. See
            :ref:`pandas io <io.parquet>` for more details.

        See Also
        --------
        read_parquet : Read a parquet file.
        DataFrame.to_csv : Write a csv file.
        DataFrame.to_sql : Write to a sql table.
        DataFrame.to_hdf : Write to hdf.

        Notes
        -----
        This function requires either the `fastparquet
        <https://pypi.org/project/fastparquet>`_ or `pyarrow
        <https://arrow.apache.org/docs/python/>`_ library.

        Examples
        --------
        >>> df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        >>> df.to_parquet('df.parquet.gzip', compression='gzip')
        >>> pd.read_parquet('df.parquet.gzip')
           col1  col2
        0     1     3
        1     2     4
        """
        from pandas.io.parquet import to_parquet
        to_parquet(self, fname, engine,
                   compression=compression, **kwargs)
