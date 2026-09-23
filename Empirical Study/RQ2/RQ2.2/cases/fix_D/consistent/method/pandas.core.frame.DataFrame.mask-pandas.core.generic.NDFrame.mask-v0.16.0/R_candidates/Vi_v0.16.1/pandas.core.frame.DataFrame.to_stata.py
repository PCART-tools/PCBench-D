    def to_stata(
        self, fname, convert_dates=None, write_index=True, encoding="latin-1",
            byteorder=None, time_stamp=None, data_label=None):
        """
        A class for writing Stata binary dta files from array-like objects

        Parameters
        ----------
        fname : file path or buffer
            Where to save the dta file.
        convert_dates : dict
            Dictionary mapping column of datetime types to the stata internal
            format that you want to use for the dates. Options are
            'tc', 'td', 'tm', 'tw', 'th', 'tq', 'ty'. Column can be either a
            number or a name.
        encoding : str
            Default is latin-1. Note that Stata does not support unicode.
        byteorder : str
            Can be ">", "<", "little", or "big". The default is None which uses
            `sys.byteorder`

        Examples
        --------
        >>> writer = StataWriter('./data_file.dta', data)
        >>> writer.write_file()

        Or with dates

        >>> writer = StataWriter('./date_data_file.dta', data, {2 : 'tw'})
        >>> writer.write_file()
        """
        from pandas.io.stata import StataWriter
        writer = StataWriter(fname, self, convert_dates=convert_dates,
                             encoding=encoding, byteorder=byteorder,
                             time_stamp=time_stamp, data_label=data_label,
                             write_index=write_index)
        writer.write_file()
