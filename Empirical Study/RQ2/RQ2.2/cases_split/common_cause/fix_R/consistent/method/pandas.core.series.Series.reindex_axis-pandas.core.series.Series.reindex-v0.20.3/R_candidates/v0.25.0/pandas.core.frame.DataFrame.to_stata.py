    @deprecate_kwarg(old_arg_name="encoding", new_arg_name=None)
    def to_stata(
        self,
        fname,
        convert_dates=None,
        write_index=True,
        encoding="latin-1",
        byteorder=None,
        time_stamp=None,
        data_label=None,
        variable_labels=None,
        version=114,
        convert_strl=None,
    ):
        """
        Export DataFrame object to Stata dta format.

        Writes the DataFrame to a Stata dataset file.
        "dta" files contain a Stata dataset.

        Parameters
        ----------
        fname : str, buffer or path object
            String, path object (pathlib.Path or py._path.local.LocalPath) or
            object implementing a binary write() function. If using a buffer
            then the buffer will not be automatically closed after the file
            data has been written.
        convert_dates : dict
            Dictionary mapping columns containing datetime types to stata
            internal format to use when writing the dates. Options are 'tc',
            'td', 'tm', 'tw', 'th', 'tq', 'ty'. Column can be either an integer
            or a name. Datetime columns that do not have a conversion type
            specified will be converted to 'tc'. Raises NotImplementedError if
            a datetime column has timezone information.
        write_index : bool
            Write the index to Stata dataset.
        encoding : str
            Default is latin-1. Unicode is not supported.
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

            .. versionadded:: 0.19.0

        version : {114, 117}, default 114
            Version to use in the output dta file.  Version 114 can be used
            read by Stata 10 and later.  Version 117 can be read by Stata 13
            or later. Version 114 limits string variables to 244 characters or
            fewer while 117 allows strings with lengths up to 2,000,000
            characters.

            .. versionadded:: 0.23.0

        convert_strl : list, optional
            List of column names to convert to string columns to Stata StrL
            format. Only available if version is 117.  Storing strings in the
            StrL format can produce smaller dta files if strings have more than
            8 characters and values are repeated.

            .. versionadded:: 0.23.0

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

            .. versionadded:: 0.19.0

        See Also
        --------
        read_stata : Import Stata data files.
        io.stata.StataWriter : Low-level writer for Stata data files.
        io.stata.StataWriter117 : Low-level writer for version 117 files.

        Examples
        --------
        >>> df = pd.DataFrame({'animal': ['falcon', 'parrot', 'falcon',
        ...                               'parrot'],
        ...                    'speed': [350, 18, 361, 15]})
        >>> df.to_stata('animals.dta')  # doctest: +SKIP
        """
        kwargs = {}
        if version not in (114, 117):
            raise ValueError("Only formats 114 and 117 supported.")
        if version == 114:
            if convert_strl is not None:
                raise ValueError(
                    "strl support is only available when using " "format 117"
                )
            from pandas.io.stata import StataWriter as statawriter
        else:
            from pandas.io.stata import StataWriter117 as statawriter

            kwargs["convert_strl"] = convert_strl

        writer = statawriter(
            fname,
            self,
            convert_dates=convert_dates,
            byteorder=byteorder,
            time_stamp=time_stamp,
            data_label=data_label,
            write_index=write_index,
            variable_labels=variable_labels,
            **kwargs
        )
        writer.write_file()
