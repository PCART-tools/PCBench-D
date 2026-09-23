    @classmethod
    def from_csv(cls, path, header=0, sep=',', index_col=0, parse_dates=True,
                 encoding=None, tupleize_cols=None,
                 infer_datetime_format=False):
        """
        Read CSV file (DEPRECATED, please use :func:`pandas.read_csv`
        instead).

        It is preferable to use the more powerful :func:`pandas.read_csv`
        for most general purposes, but ``from_csv`` makes for an easy
        roundtrip to and from a file (the exact counterpart of
        ``to_csv``), especially with a DataFrame of time series data.

        This method only differs from the preferred :func:`pandas.read_csv`
        in some defaults:

        - `index_col` is ``0`` instead of ``None`` (take first column as index
          by default)
        - `parse_dates` is ``True`` instead of ``False`` (try parsing the index
          as datetime by default)

        So a ``pd.DataFrame.from_csv(path)`` can be replaced by
        ``pd.read_csv(path, index_col=0, parse_dates=True)``.

        Parameters
        ----------
        path : string file path or file handle / StringIO
        header : int, default 0
            Row to use as header (skip prior rows)
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
        infer_datetime_format: boolean, default False
            If True and `parse_dates` is True for a column, try to infer the
            datetime format based on the first datetime string. If the format
            can be inferred, there often will be a large parsing speed-up.

        See also
        --------
        pandas.read_csv

        Returns
        -------
        y : DataFrame

        """

        warnings.warn("from_csv is deprecated. Please use read_csv(...) "
                      "instead. Note that some of the default arguments are "
                      "different, so please refer to the documentation "
                      "for from_csv when changing your function calls",
                      FutureWarning, stacklevel=2)

        from pandas.io.parsers import read_table
        return read_table(path, header=header, sep=sep,
                          parse_dates=parse_dates, index_col=index_col,
                          encoding=encoding, tupleize_cols=tupleize_cols,
                          infer_datetime_format=infer_datetime_format)
