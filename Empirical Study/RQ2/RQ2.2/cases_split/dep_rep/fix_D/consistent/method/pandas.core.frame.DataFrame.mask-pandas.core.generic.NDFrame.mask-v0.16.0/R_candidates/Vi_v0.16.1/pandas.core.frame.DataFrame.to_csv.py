    def to_csv(self, path_or_buf=None, sep=",", na_rep='', float_format=None,
               columns=None, header=True, index=True, index_label=None,
               mode='w', encoding=None, quoting=None,
               quotechar='"', line_terminator='\n', chunksize=None,
               tupleize_cols=False, date_format=None, doublequote=True,
               escapechar=None, decimal='.', **kwds):
        r"""Write DataFrame to a comma-separated values (csv) file

        Parameters
        ----------
        path_or_buf : string or file handle, default None
            File path or object, if None is provided the result is returned as
            a string.
        sep : character, default ","
            Field delimiter for the output file.
        na_rep : string, default ''
            Missing data representation
        float_format : string, default None
            Format string for floating point numbers
        columns : sequence, optional
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
            A string representing the encoding to use in the output file,
            defaults to 'ascii' on Python 2 and 'utf-8' on Python 3.
        line_terminator : string, default '\\n'
            The newline character or character sequence to use in the output
            file
        quoting : optional constant from csv module
            defaults to csv.QUOTE_MINIMAL
        quotechar : string (length 1), default '"'
            character used to quote fields
        doublequote : boolean, default True
            Control quoting of `quotechar` inside a field
        escapechar : string (length 1), default None
            character used to escape `sep` and `quotechar` when appropriate
        chunksize : int or None
            rows to write at a time
        tupleize_cols : boolean, default False
            write multi_index columns as a list of tuples (if True)
            or new (expanded format) if False)
        date_format : string, default None
            Format string for datetime objects
        decimal: string, default '.'
            Character recognized as decimal separator. E.g. use ',' for European data
        """

        formatter = fmt.CSVFormatter(self, path_or_buf,
                                     line_terminator=line_terminator,
                                     sep=sep, encoding=encoding,
                                     quoting=quoting, na_rep=na_rep,
                                     float_format=float_format, cols=columns,
                                     header=header, index=index,
                                     index_label=index_label, mode=mode,
                                     chunksize=chunksize, quotechar=quotechar,
                                     engine=kwds.get("engine"),
                                     tupleize_cols=tupleize_cols,
                                     date_format=date_format,
                                     doublequote=doublequote,
                                     escapechar=escapechar,
                                     decimal=decimal)
        formatter.save()

        if path_or_buf is None:
            return formatter.path_or_buf.getvalue()
