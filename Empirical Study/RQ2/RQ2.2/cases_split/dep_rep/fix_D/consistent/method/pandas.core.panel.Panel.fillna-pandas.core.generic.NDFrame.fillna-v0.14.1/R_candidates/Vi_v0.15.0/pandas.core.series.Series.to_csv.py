    def to_csv(self, path, index=True, sep=",", na_rep='',
               float_format=None, header=False,
               index_label=None, mode='w', nanRep=None, encoding=None,
               date_format=None):
        """
        Write Series to a comma-separated values (csv) file

        Parameters
        ----------
        path : string file path or file handle / StringIO. If None is provided
            the result is returned as a string.
        na_rep : string, default ''
            Missing data representation
        float_format : string, default None
            Format string for floating point numbers
        header : boolean, default False
            Write out series name
        index : boolean, default True
            Write row names (index)
        index_label : string or sequence, default None
            Column label for index column(s) if desired. If None is given, and
            `header` and `index` are True, then the index names are used. A
            sequence should be given if the DataFrame uses MultiIndex.
        mode : Python write mode, default 'w'
        sep : character, default ","
            Field delimiter for the output file.
        encoding : string, optional
            a string representing the encoding to use if the contents are
            non-ascii, for python versions prior to 3
        date_format: string, default None
            Format string for datetime objects.
        """
        from pandas.core.frame import DataFrame
        df = DataFrame(self)
        # result is only a string if no path provided, otherwise None
        result = df.to_csv(path, index=index, sep=sep, na_rep=na_rep,
                  float_format=float_format, header=header,
                  index_label=index_label, mode=mode, nanRep=nanRep,
                  encoding=encoding, date_format=date_format)
        if path is None:
            return result
