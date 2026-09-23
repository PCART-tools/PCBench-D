    def info(self, verbose=None, buf=None, max_cols=None):
        """
        Concise summary of a DataFrame.

        Parameters
        ----------
        verbose : {None, True, False}, optional
            Whether to print the full summary.
            None follows the `display.max_info_columns` setting.
            True or False overrides the `display.max_info_columns` setting.
        buf : writable buffer, defaults to sys.stdout
        max_cols : int, default None
            Determines whether full summary or short summary is printed.
            None follows the `display.max_info_columns` setting.
        """
        from pandas.core.format import _put_lines

        if buf is None:  # pragma: no cover
            buf = sys.stdout

        lines = []

        lines.append(str(type(self)))
        lines.append(self.index.summary())

        if len(self.columns) == 0:
            lines.append('Empty %s' % type(self).__name__)
            _put_lines(buf, lines)
            return

        cols = self.columns

        # hack
        if max_cols is None:
            max_cols = get_option(
                'display.max_info_columns', len(self.columns) + 1)

        max_rows = get_option('display.max_info_rows', len(self) + 1)

        show_counts = ((len(self.columns) <= max_cols) and
                       (len(self) < max_rows))
        exceeds_info_cols = len(self.columns) > max_cols

        def _verbose_repr():
            lines.append('Data columns (total %d columns):' %
                         len(self.columns))
            space = max([len(com.pprint_thing(k)) for k in self.columns]) + 4
            counts = None

            tmpl = "%s%s"
            if show_counts:
                counts = self.count()
                if len(cols) != len(counts):  # pragma: no cover
                    raise AssertionError('Columns must equal counts (%d != %d)' %
                                         (len(cols), len(counts)))
                tmpl = "%s non-null %s"

            dtypes = self.dtypes
            for i, col in enumerate(self.columns):
                dtype = dtypes[col]
                col = com.pprint_thing(col)

                count = ""
                if show_counts:
                    count = counts.iloc[i]

                lines.append(_put_str(col, space) +
                             tmpl % (count, dtype))

        def _non_verbose_repr():
            lines.append(self.columns.summary(name='Columns'))

        if verbose:
            _verbose_repr()
        elif verbose is False:  # specifically set to False, not nesc None
            _non_verbose_repr()
        else:
            if exceeds_info_cols:
                _non_verbose_repr()
            else:
                _verbose_repr()

        counts = self.get_dtype_counts()
        dtypes = ['%s(%d)' % k for k in sorted(compat.iteritems(counts))]
        lines.append('dtypes: %s' % ', '.join(dtypes))
        _put_lines(buf, lines)
