    @final
    @doc(
        storage_options=_shared_docs["storage_options"],
        compression_options=_shared_docs["compression_options"] % "path_or_buf",
    )
    def to_csv(
        self,
        path_or_buf: FilePath | WriteBuffer[bytes] | WriteBuffer[str] | None = None,
        sep: str = ",",
        na_rep: str = "",
        float_format: str | Callable | None = None,
        columns: Sequence[Hashable] | None = None,
        header: bool_t | list[str] = True,
        index: bool_t = True,
        index_label: IndexLabel | None = None,
        mode: str = "w",
        encoding: str | None = None,
        compression: CompressionOptions = "infer",
        quoting: int | None = None,
        quotechar: str = '"',
        lineterminator: str | None = None,
        chunksize: int | None = None,
        date_format: str | None = None,
        doublequote: bool_t = True,
        escapechar: str | None = None,
        decimal: str = ".",
        errors: str = "strict",
        storage_options: StorageOptions = None,
    ) -> str | None:
        r"""
        Write object to a comma-separated values (csv) file.

        Parameters
        ----------
        path_or_buf : str, path object, file-like object, or None, default None
            String, path object (implementing os.PathLike[str]), or file-like
            object implementing a write() function. If None, the result is
            returned as a string. If a non-binary file object is passed, it should
            be opened with `newline=''`, disabling universal newlines. If a binary
            file object is passed, `mode` might need to contain a `'b'`.

            .. versionchanged:: 1.2.0

               Support for binary file objects was introduced.

        sep : str, default ','
            String of length 1. Field delimiter for the output file.
        na_rep : str, default ''
            Missing data representation.
        float_format : str, Callable, default None
            Format string for floating point numbers. If a Callable is given, it takes
            precedence over other numeric formatting parameters, like decimal.
        columns : sequence, optional
            Columns to write.
        header : bool or list of str, default True
            Write out the column names. If a list of strings is given it is
            assumed to be aliases for the column names.
        index : bool, default True
            Write row names (index).
        index_label : str or sequence, or False, default None
            Column label for index column(s) if desired. If None is given, and
            `header` and `index` are True, then the index names are used. A
            sequence should be given if the object uses MultiIndex. If
            False do not print fields for index names. Use index_label=False
            for easier importing in R.
        mode : str, default 'w'
            Python write mode. The available write modes are the same as
            :py:func:`open`.
        encoding : str, optional
            A string representing the encoding to use in the output file,
            defaults to 'utf-8'. `encoding` is not supported if `path_or_buf`
            is a non-binary file object.
        {compression_options}

            .. versionchanged:: 1.0.0

               May now be a dict with key 'method' as compression mode
               and other entries as additional compression options if
               compression mode is 'zip'.

            .. versionchanged:: 1.1.0

               Passing compression options as keys in dict is
               supported for compression modes 'gzip', 'bz2', 'zstd', and 'zip'.

            .. versionchanged:: 1.2.0

                Compression is supported for binary file objects.

            .. versionchanged:: 1.2.0

                Previous versions forwarded dict entries for 'gzip' to
                `gzip.open` instead of `gzip.GzipFile` which prevented
                setting `mtime`.

        quoting : optional constant from csv module
            Defaults to csv.QUOTE_MINIMAL. If you have set a `float_format`
            then floats are converted to strings and thus csv.QUOTE_NONNUMERIC
            will treat them as non-numeric.
        quotechar : str, default '\"'
            String of length 1. Character used to quote fields.
        lineterminator : str, optional
            The newline character or character sequence to use in the output
            file. Defaults to `os.linesep`, which depends on the OS in which
            this method is called ('\\n' for linux, '\\r\\n' for Windows, i.e.).

            .. versionchanged:: 1.5.0

                Previously was line_terminator, changed for consistency with
                read_csv and the standard library 'csv' module.

        chunksize : int or None
            Rows to write at a time.
        date_format : str, default None
            Format string for datetime objects.
        doublequote : bool, default True
            Control quoting of `quotechar` inside a field.
        escapechar : str, default None
            String of length 1. Character used to escape `sep` and `quotechar`
            when appropriate.
        decimal : str, default '.'
            Character recognized as decimal separator. E.g. use ',' for
            European data.
        errors : str, default 'strict'
            Specifies how encoding and decoding errors are to be handled.
            See the errors argument for :func:`open` for a full list
            of options.

            .. versionadded:: 1.1.0

        {storage_options}

            .. versionadded:: 1.2.0

        Returns
        -------
        None or str
            If path_or_buf is None, returns the resulting csv format as a
            string. Otherwise returns None.

        See Also
        --------
        read_csv : Load a CSV file into a DataFrame.
        to_excel : Write DataFrame to an Excel file.

        Examples
        --------
        >>> df = pd.DataFrame({{'name': ['Raphael', 'Donatello'],
        ...                    'mask': ['red', 'purple'],
        ...                    'weapon': ['sai', 'bo staff']}})
        >>> df.to_csv(index=False)
        'name,mask,weapon\nRaphael,red,sai\nDonatello,purple,bo staff\n'

        Create 'out.zip' containing 'out.csv'

        >>> compression_opts = dict(method='zip',
        ...                         archive_name='out.csv')  # doctest: +SKIP
        >>> df.to_csv('out.zip', index=False,
        ...           compression=compression_opts)  # doctest: +SKIP

        To write a csv file to a new folder or nested folder you will first
        need to create it using either Pathlib or os:

        >>> from pathlib import Path  # doctest: +SKIP
        >>> filepath = Path('folder/subfolder/out.csv')  # doctest: +SKIP
        >>> filepath.parent.mkdir(parents=True, exist_ok=True)  # doctest: +SKIP
        >>> df.to_csv(filepath)  # doctest: +SKIP

        >>> import os  # doctest: +SKIP
        >>> os.makedirs('folder/subfolder', exist_ok=True)  # doctest: +SKIP
        >>> df.to_csv('folder/subfolder/out.csv')  # doctest: +SKIP
        """
        df = self if isinstance(self, ABCDataFrame) else self.to_frame()

        formatter = DataFrameFormatter(
            frame=df,
            header=header,
            index=index,
            na_rep=na_rep,
            float_format=float_format,
            decimal=decimal,
        )

        return DataFrameRenderer(formatter).to_csv(
            path_or_buf,
            lineterminator=lineterminator,
            sep=sep,
            encoding=encoding,
            errors=errors,
            compression=compression,
            quoting=quoting,
            columns=columns,
            index_label=index_label,
            mode=mode,
            chunksize=chunksize,
            quotechar=quotechar,
            date_format=date_format,
            doublequote=doublequote,
            escapechar=escapechar,
            storage_options=storage_options,
        )
