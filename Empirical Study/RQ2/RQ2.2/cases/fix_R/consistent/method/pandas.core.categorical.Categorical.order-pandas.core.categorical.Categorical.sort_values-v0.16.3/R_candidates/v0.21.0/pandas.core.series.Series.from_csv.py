    @classmethod
    def from_csv(cls, path, sep=',', parse_dates=True, header=None,
                 index_col=0, encoding=None, infer_datetime_format=False):
        """
        Read CSV file (DEPRECATED, please use :func:`pandas.read_csv`
        instead).

        It is preferable to use the more powerful :func:`pandas.read_csv`
        for most general purposes, but ``from_csv`` makes for an easy
        roundtrip to and from a file (the exact counterpart of
        ``to_csv``), especially with a time Series.

        This method only differs from :func:`pandas.read_csv` in some defaults:

        - `index_col` is ``0`` instead of ``None`` (take first column as index
          by default)
        - `header` is ``None`` instead of ``0`` (the first row is not used as
          the column names)
        - `parse_dates` is ``True`` instead of ``False`` (try parsing the index
          as datetime by default)

        With :func:`pandas.read_csv`, the option ``squeeze=True`` can be used
        to return a Series like ``from_csv``.

        Parameters
        ----------
        path : string file path or file handle / StringIO
        sep : string, default ','
            Field delimiter
        parse_dates : boolean, default True
            Parse dates. Different default from read_table
        header : int, default None
            Row to use as header (skip prior rows)
        index_col : int or sequence, default 0
            Column to use for index. If a sequence is given, a MultiIndex
            is used. Different default from read_table
        encoding : string, optional
            a string representing the encoding to use if the contents are
            non-ascii, for python versions prior to 3
        infer_datetime_format: boolean, default False
            If True and `parse_dates` is True for a column, try to infer the
            datetime format based on the first datetime string. If the format
            can be inferred, there often will be a large parsing speed-up.

        See also
        --------
        pandas.read_csv

        Returns
        -------
        y : Series
        """

        # We're calling `DataFrame.from_csv` in the implementation,
        # which will propagate a warning regarding `from_csv` deprecation.
        from pandas.core.frame import DataFrame
        df = DataFrame.from_csv(path, header=header, index_col=index_col,
                                sep=sep, parse_dates=parse_dates,
                                encoding=encoding,
                                infer_datetime_format=infer_datetime_format)
        result = df.iloc[:, 0]
        if header is None:
            result.index.name = result.name = None

        return result
