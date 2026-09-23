    def to_pickle(self, path, compression='infer',
                  protocol=pkl.HIGHEST_PROTOCOL):
        """
        Pickle (serialize) object to file.

        Parameters
        ----------
        path : str
            File path where the pickled object will be stored.
        compression : {'infer', 'gzip', 'bz2', 'zip', 'xz', None}, \
        default 'infer'
            A string representing the compression to use in the output file. By
            default, infers from the file extension in specified path.

            .. versionadded:: 0.20.0
        protocol : int
            Int which indicates which protocol should be used by the pickler,
            default HIGHEST_PROTOCOL (see [1]_ paragraph 12.1.2). The possible
            values for this parameter depend on the version of Python. For
            Python 2.x, possible values are 0, 1, 2. For Python>=3.0, 3 is a
            valid value. For Python >= 3.4, 4 is a valid value. A negative
            value for the protocol parameter is equivalent to setting its value
            to HIGHEST_PROTOCOL.

            .. [1] https://docs.python.org/3/library/pickle.html
            .. versionadded:: 0.21.0

        See Also
        --------
        read_pickle : Load pickled pandas object (or any object) from file.
        DataFrame.to_hdf : Write DataFrame to an HDF5 file.
        DataFrame.to_sql : Write DataFrame to a SQL database.
        DataFrame.to_parquet : Write a DataFrame to the binary parquet format.

        Examples
        --------
        >>> original_df = pd.DataFrame({"foo": range(5), "bar": range(5, 10)})
        >>> original_df
           foo  bar
        0    0    5
        1    1    6
        2    2    7
        3    3    8
        4    4    9
        >>> original_df.to_pickle("./dummy.pkl")

        >>> unpickled_df = pd.read_pickle("./dummy.pkl")
        >>> unpickled_df
           foo  bar
        0    0    5
        1    1    6
        2    2    7
        3    3    8
        4    4    9

        >>> import os
        >>> os.remove("./dummy.pkl")
        """
        from pandas.io.pickle import to_pickle
        return to_pickle(self, path, compression=compression,
                         protocol=protocol)
