    def to_pickle(self, path, compression='infer',
                  protocol=pkl.HIGHEST_PROTOCOL):
        """
        Pickle (serialize) object to input file path.

        Parameters
        ----------
        path : string
            File path
        compression : {'infer', 'gzip', 'bz2', 'xz', None}, default 'infer'
            a string representing the compression to use in the output file

            .. versionadded:: 0.20.0
        protocol : int
            Int which indicates which protocol should be used by the pickler,
            default HIGHEST_PROTOCOL (see [1], paragraph 12.1.2). The possible
            values for this parameter depend on the version of Python. For
            Python 2.x, possible values are 0, 1, 2. For Python>=3.0, 3 is a
            valid value. For Python >= 3.4, 4 is a valid value.A negative value
            for the protocol parameter is equivalent to setting its value to
            HIGHEST_PROTOCOL.

            .. [1] https://docs.python.org/3/library/pickle.html
            .. versionadded:: 0.21.0

        """
        from pandas.io.pickle import to_pickle
        return to_pickle(self, path, compression=compression,
                         protocol=protocol)
