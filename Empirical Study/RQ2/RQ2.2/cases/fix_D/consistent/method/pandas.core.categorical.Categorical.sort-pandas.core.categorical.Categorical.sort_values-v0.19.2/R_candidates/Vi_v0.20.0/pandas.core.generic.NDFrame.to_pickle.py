    def to_pickle(self, path, compression='infer'):
        """
        Pickle (serialize) object to input file path.

        Parameters
        ----------
        path : string
            File path
        compression : {'infer', 'gzip', 'bz2', 'xz', None}, default 'infer'
            a string representing the compression to use in the output file

            .. versionadded:: 0.20.0
        """
        from pandas.io.pickle import to_pickle
        return to_pickle(self, path, compression=compression)
