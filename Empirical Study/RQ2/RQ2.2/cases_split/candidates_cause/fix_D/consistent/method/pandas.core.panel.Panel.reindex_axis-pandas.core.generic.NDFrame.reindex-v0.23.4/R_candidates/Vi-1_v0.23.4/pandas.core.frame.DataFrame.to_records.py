    def to_records(self, index=True, convert_datetime64=None):
        """
        Convert DataFrame to a NumPy record array.

        Index will be put in the 'index' field of the record array if
        requested.

        Parameters
        ----------
        index : boolean, default True
            Include index in resulting record array, stored in 'index' field.
        convert_datetime64 : boolean, default None
            .. deprecated:: 0.23.0

            Whether to convert the index to datetime.datetime if it is a
            DatetimeIndex.

        Returns
        -------
        y : numpy.recarray

        See Also
        --------
        DataFrame.from_records: convert structured or record ndarray
            to DataFrame.
        numpy.recarray: ndarray that allows field access using
            attributes, analogous to typed columns in a
            spreadsheet.

        Examples
        --------
        >>> df = pd.DataFrame({'A': [1, 2], 'B': [0.5, 0.75]},
        ...                   index=['a', 'b'])
        >>> df
           A     B
        a  1  0.50
        b  2  0.75
        >>> df.to_records()
        rec.array([('a', 1, 0.5 ), ('b', 2, 0.75)],
                  dtype=[('index', 'O'), ('A', '<i8'), ('B', '<f8')])

        The index can be excluded from the record array:

        >>> df.to_records(index=False)
        rec.array([(1, 0.5 ), (2, 0.75)],
                  dtype=[('A', '<i8'), ('B', '<f8')])

        By default, timestamps are converted to `datetime.datetime`:

        >>> df.index = pd.date_range('2018-01-01 09:00', periods=2, freq='min')
        >>> df
                             A     B
        2018-01-01 09:00:00  1  0.50
        2018-01-01 09:01:00  2  0.75
        >>> df.to_records()
        rec.array([(datetime.datetime(2018, 1, 1, 9, 0), 1, 0.5 ),
                   (datetime.datetime(2018, 1, 1, 9, 1), 2, 0.75)],
                  dtype=[('index', 'O'), ('A', '<i8'), ('B', '<f8')])

        The timestamp conversion can be disabled so NumPy's datetime64
        data type is used instead:

        >>> df.to_records(convert_datetime64=False)
        rec.array([('2018-01-01T09:00:00.000000000', 1, 0.5 ),
                   ('2018-01-01T09:01:00.000000000', 2, 0.75)],
                  dtype=[('index', '<M8[ns]'), ('A', '<i8'), ('B', '<f8')])
        """

        if convert_datetime64 is not None:
            warnings.warn("The 'convert_datetime64' parameter is "
                          "deprecated and will be removed in a future "
                          "version",
                          FutureWarning, stacklevel=2)

        if index:
            if is_datetime64_any_dtype(self.index) and convert_datetime64:
                ix_vals = [self.index.to_pydatetime()]
            else:
                if isinstance(self.index, MultiIndex):
                    # array of tuples to numpy cols. copy copy copy
                    ix_vals = lmap(np.array, zip(*self.index.values))
                else:
                    ix_vals = [self.index.values]

            arrays = ix_vals + [self[c].get_values() for c in self.columns]

            count = 0
            index_names = list(self.index.names)
            if isinstance(self.index, MultiIndex):
                for i, n in enumerate(index_names):
                    if n is None:
                        index_names[i] = 'level_%d' % count
                        count += 1
            elif index_names[0] is None:
                index_names = ['index']
            names = (lmap(compat.text_type, index_names) +
                     lmap(compat.text_type, self.columns))
        else:
            arrays = [self[c].get_values() for c in self.columns]
            names = lmap(compat.text_type, self.columns)

        formats = [v.dtype for v in arrays]
        return np.rec.fromarrays(
            arrays,
            dtype={'names': names, 'formats': formats}
        )
