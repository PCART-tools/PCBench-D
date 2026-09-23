    def to_csv(self, path_or_buf, sep=",", na_rep='', float_format=None,
               cols=None, header=True, index=True, index_label=None,
               mode='w', nanRep=None, encoding=None, quoting=None,
               line_terminator='\n', chunksize=None,
               tupleize_cols=False, date_format=None, **kwds):
        r"""Write DataFrame to a comma-separated values (csv) file

        Parameters
        ----------
        path_or_buf : string or file handle / StringIO
            File path
        sep : character, default ","
            Field delimiter for the output file.
        na_rep : string, default ''
            Missing data representation
        float_format : string, default None
            Format string for floating point numbers
        cols : sequence, optional
            Columns to write
        header : boolean or list of string, default True
            Write out column names. If a list of string is given it is assumed
            to be aliases for the column names
        index : boolean, default True
            Write row names (index)
        index_label : string or sequence, or False, default None
            Column label for index column(s) if desired. If None is given, and
            `header` and `index` are True, then the index names are used. A
            sequence should be given if the DataFrame uses MultiIndex.  If
            False do not print fields for index names. Use index_label=False
            for easier importing in R
        nanRep : None
            deprecated, use na_rep
        mode : str
            Python write mode, default 'w'
        encoding : string, optional
            a string representing the encoding to use if the contents are
            non-ascii, for python versions prior to 3
        line_terminator : string, default '\\n'
            The newline character or character sequence to use in the output
            file
        quoting : optional constant from csv module
            defaults to csv.QUOTE_MINIMAL
        chunksize : int or None
            rows to write at a time
        tupleize_cols : boolean, default False
            write multi_index columns as a list of tuples (if True)
            or new (expanded format) if False)
        date_format : string, default None
            Format string for datetime objects.
        """
        if nanRep is not None:  # pragma: no cover
            warnings.warn("nanRep is deprecated, use na_rep",
                          FutureWarning)
            na_rep = nanRep

        formatter = fmt.CSVFormatter(self, path_or_buf,
                                     line_terminator=line_terminator,
                                     sep=sep, encoding=encoding,
                                     quoting=quoting, na_rep=na_rep,
                                     float_format=float_format, cols=cols,
                                     header=header, index=index,
                                     index_label=index_label, mode=mode,
                                     chunksize=chunksize, engine=kwds.get(
                                         "engine"),
                                     tupleize_cols=tupleize_cols,
                                     date_format=date_format)
        formatter.save()
