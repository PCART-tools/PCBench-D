    @doc(
        storage_options=_shared_docs["storage_options"],
        compression_options=_shared_docs["compression_options"] % "path",
    )
    @deprecate_kwarg(old_arg_name="fname", new_arg_name="path")
    def to_stata(
        self,
        path: FilePath | WriteBuffer[bytes],
        convert_dates: dict[Hashable, str] | None = None,
        write_index: bool = True,
        byteorder: str | None = None,
        time_stamp: datetime.datetime | None = None,
        data_label: str | None = None,
        variable_labels: dict[Hashable, str] | None = None,
        version: int | None = 114,
        convert_strl: Sequence[Hashable] | None = None,
        compression: CompressionOptions = "infer",
        storage_options: StorageOptions = None,
        *,
        value_labels: dict[Hashable, dict[float | int, str]] | None = None,
    ) -> None:
        """
        Export DataFrame object to Stata dta format.

        Writes the DataFrame to a Stata dataset file.
        "dta" files contain a Stata dataset.

        Parameters
        ----------
        path : str, path object, or buffer
            String, path object (implementing ``os.PathLike[str]``), or file-like
            object implementing a binary ``write()`` function.

            .. versionchanged:: 1.0.0

            Previously this was "fname"

        convert_dates : dict
            Dictionary mapping columns containing datetime types to stata
            internal format to use when writing the dates. Options are 'tc',
            'td', 'tm', 'tw', 'th', 'tq', 'ty'. Column can be either an integer
            or a name. Datetime columns that do not have a conversion type
            specified will be converted to 'tc'. Raises NotImplementedError if
            a datetime column has timezone information.
        write_index : bool
            Write the index to Stata dataset.
        byteorder : str
            Can be ">", "<", "little", or "big". default is `sys.byteorder`.
        time_stamp : datetime
            A datetime to use as file creation date.  Default is the current
            time.
        data_label : str, optional
            A label for the data set.  Must be 80 characters or smaller.
        variable_labels : dict
            Dictionary containing columns as keys and variable labels as
            values. Each label must be 80 characters or smaller.
        version : {{114, 117, 118, 119, None}}, default 114
            Version to use in the output dta file. Set to None to let pandas
            decide between 118 or 119 formats depending on the number of
            columns in the frame. Version 114 can be read by Stata 10 and
            later. Version 117 can be read by Stata 13 or later. Version 118
            is supported in Stata 14 and later. Version 119 is supported in
            Stata 15 and later. Version 114 limits string variables to 244
            characters or fewer while versions 117 and later allow strings
            with lengths up to 2,000,000 characters. Versions 118 and 119
            support Unicode characters, and version 119 supports more than
            32,767 variables.

            Version 119 should usually only be used when the number of
            variables exceeds the capacity of dta format 118. Exporting
            smaller datasets in format 119 may have unintended consequences,
            and, as of November 2020, Stata SE cannot read version 119 files.

            .. versionchanged:: 1.0.0

                Added support for formats 118 and 119.

        convert_strl : list, optional
            List of column names to convert to string columns to Stata StrL
            format. Only available if version is 117.  Storing strings in the
            StrL format can produce smaller dta files if strings have more than
            8 characters and values are repeated.
        {compression_options}

            .. versionadded:: 1.1.0

            .. versionchanged:: 1.4.0 Zstandard support.

        {storage_options}

            .. versionadded:: 1.2.0

        value_labels : dict of dicts
            Dictionary containing columns as keys and dictionaries of column value
            to labels as values. Labels for a single variable must be 32,000
            characters or smaller.

            .. versionadded:: 1.4.0

        Raises
        ------
        NotImplementedError
            * If datetimes contain timezone information
            * Column dtype is not representable in Stata
        ValueError
            * Columns listed in convert_dates are neither datetime64[ns]
              or datetime.datetime
            * Column listed in convert_dates is not in DataFrame
            * Categorical label contains more than 32,000 characters

        See Also
        --------
        read_stata : Import Stata data files.
        io.stata.StataWriter : Low-level writer for Stata data files.
        io.stata.StataWriter117 : Low-level writer for version 117 files.

        Examples
        --------
        >>> df = pd.DataFrame({{'animal': ['falcon', 'parrot', 'falcon',
        ...                               'parrot'],
        ...                    'speed': [350, 18, 361, 15]}})
        >>> df.to_stata('animals.dta')  # doctest: +SKIP
        """
        if version not in (114, 117, 118, 119, None):
            raise ValueError("Only formats 114, 117, 118 and 119 are supported.")
        if version == 114:
            if convert_strl is not None:
                raise ValueError("strl is not supported in format 114")
            from pandas.io.stata import StataWriter as statawriter
        elif version == 117:
            # mypy: Name 'statawriter' already defined (possibly by an import)
            from pandas.io.stata import (  # type: ignore[no-redef]
                StataWriter117 as statawriter,
            )
        else:  # versions 118 and 119
            # mypy: Name 'statawriter' already defined (possibly by an import)
            from pandas.io.stata import (  # type: ignore[no-redef]
                StataWriterUTF8 as statawriter,
            )

        kwargs: dict[str, Any] = {}
        if version is None or version >= 117:
            # strl conversion is only supported >= 117
            kwargs["convert_strl"] = convert_strl
        if version is None or version >= 118:
            # Specifying the version is only supported for UTF8 (118 or 119)
            kwargs["version"] = version

        writer = statawriter(
            path,
            self,
            convert_dates=convert_dates,
            byteorder=byteorder,
            time_stamp=time_stamp,
            data_label=data_label,
            write_index=write_index,
            variable_labels=variable_labels,
            compression=compression,
            storage_options=storage_options,
            value_labels=value_labels,
            **kwargs,
        )
        writer.write_file()
