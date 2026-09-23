    def to_excel(self, path, na_rep='', engine=None, **kwargs):
        """
        Write each DataFrame in Panel to a separate excel sheet

        Parameters
        ----------
        path : string or ExcelWriter object
            File path or existing ExcelWriter
        na_rep : string, default ''
            Missing data representation
        engine : string, default None
            write engine to use - you can also set this via the options
            ``io.excel.xlsx.writer``, ``io.excel.xls.writer``, and
            ``io.excel.xlsm.writer``.

        Other Parameters
        ----------------
        float_format : string, default None
            Format string for floating point numbers
        cols : sequence, optional
            Columns to write
        header : boolean or list of string, default True
            Write out column names. If a list of string is given it is
            assumed to be aliases for the column names
        index : boolean, default True
            Write row names (index)
        index_label : string or sequence, default None
            Column label for index column(s) if desired. If None is given, and
            `header` and `index` are True, then the index names are used. A
            sequence should be given if the DataFrame uses MultiIndex.
        startrow : upper left cell row to dump data frame
        startcol : upper left cell column to dump data frame

        Notes
        -----
        Keyword arguments (and na_rep) are passed to the ``to_excel`` method
        for each DataFrame written.
        """
        from pandas.io.excel import ExcelWriter

        if isinstance(path, compat.string_types):
            writer = ExcelWriter(path, engine=engine)
        else:
            writer = path
        kwargs['na_rep'] = na_rep

        for item, df in self.iteritems():
            name = str(item)
            df.to_excel(writer, name, **kwargs)
        writer.save()
