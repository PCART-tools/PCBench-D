    @classmethod
    def from_csv(cls, path, header=0, sep=',', index_col=0,
                 parse_dates=True, encoding=None, tupleize_cols=False):
        """
        Read delimited file into DataFrame

        Parameters
        ----------
        path : string file path or file handle / StringIO
        header : int, default 0
            Row to use at header (skip prior rows)
        sep : string, default ','
            Field delimiter
        index_col : int or sequence, default 0
            Column to use for index. If a sequence is given, a MultiIndex
            is used. Different default from read_table
        parse_dates : boolean, default True
            Parse dates. Different default from read_table
        tupleize_cols : boolean, default False
            write multi_index columns as a list of tuples (if True)
            or new (expanded format) if False)

        Notes
        -----
        Preferable to use read_table for most general purposes but from_csv
        makes for an easy roundtrip to and from file, especially with a
        DataFrame of time series data

        Returns
        -------
        y : DataFrame
        """
        from pandas.io.parsers import read_table
        return read_table(path, header=header, sep=sep,
                          parse_dates=parse_dates, index_col=index_col,
                          encoding=encoding, tupleize_cols=tupleize_cols)
