    def info(self, verbose=True, buf=None, max_cols=None):
        """
        Concise summary of a DataFrame.

        Parameters
        ----------
        verbose : boolean, default True
            If False, don't print column count summary
        buf : writable buffer, defaults to sys.stdout
        max_cols : int, default None
            Determines whether full summary or short summary is printed
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

        if verbose and len(self.columns) <= max_cols:
            lines.append('Data columns (total %d columns):' %
                         len(self.columns))
            space = max([len(com.pprint_thing(k)) for k in self.columns]) + 4
            counts = self.count()
            if len(cols) != len(counts):  # pragma: no cover
                raise AssertionError('Columns must equal counts (%d != %d)' %
                                     (len(cols), len(counts)))
            for col, count in compat.iteritems(counts):
                col = com.pprint_thing(col)
                lines.append(_put_str(col, space) +
                             '%d  non-null values' % count)
        else:
            lines.append(self.columns.summary(name='Columns'))

        counts = self.get_dtype_counts()
        dtypes = ['%s(%d)' % k for k in sorted(compat.iteritems(counts))]
        lines.append('dtypes: %s' % ', '.join(dtypes))
        _put_lines(buf, lines)
