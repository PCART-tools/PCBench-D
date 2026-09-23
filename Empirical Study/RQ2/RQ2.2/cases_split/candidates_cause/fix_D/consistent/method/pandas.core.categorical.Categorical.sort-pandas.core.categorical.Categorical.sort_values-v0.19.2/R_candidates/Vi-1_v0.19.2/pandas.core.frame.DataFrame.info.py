    def info(self, verbose=None, buf=None, max_cols=None, memory_usage=None,
             null_counts=None):
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
        memory_usage : boolean/string, default None
            Specifies whether total memory usage of the DataFrame
            elements (including index) should be displayed. None follows
            the `display.memory_usage` setting. True or False overrides
            the `display.memory_usage` setting. A value of 'deep' is equivalent
            of True, with deep introspection. Memory usage is shown in
            human-readable units (base-2 representation).
        null_counts : boolean, default None
            Whether to show the non-null counts

            - If None, then only show if the frame is smaller than
              max_info_rows and max_info_columns.
            - If True, always show counts.
            - If False, never show counts.

        """
        from pandas.formats.format import _put_lines

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
            max_cols = get_option('display.max_info_columns',
                                  len(self.columns) + 1)

        max_rows = get_option('display.max_info_rows', len(self) + 1)

        if null_counts is None:
            show_counts = ((len(self.columns) <= max_cols) and
                           (len(self) < max_rows))
        else:
            show_counts = null_counts
        exceeds_info_cols = len(self.columns) > max_cols

        def _verbose_repr():
            lines.append('Data columns (total %d columns):' %
                         len(self.columns))
            space = max([len(pprint_thing(k)) for k in self.columns]) + 4
            counts = None

            tmpl = "%s%s"
            if show_counts:
                counts = self.count()
                if len(cols) != len(counts):  # pragma: no cover
                    raise AssertionError('Columns must equal counts (%d != %d)'
                                         % (len(cols), len(counts)))
                tmpl = "%s non-null %s"

            dtypes = self.dtypes
            for i, col in enumerate(self.columns):
                dtype = dtypes.iloc[i]
                col = pprint_thing(col)

                count = ""
                if show_counts:
                    count = counts.iloc[i]

                lines.append(_put_str(col, space) + tmpl % (count, dtype))

        def _non_verbose_repr():
            lines.append(self.columns.summary(name='Columns'))

        def _sizeof_fmt(num, size_qualifier):
            # returns size in human readable format
            for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
                if num < 1024.0:
                    return "%3.1f%s %s" % (num, size_qualifier, x)
                num /= 1024.0
            return "%3.1f%s %s" % (num, size_qualifier, 'PB')

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

        if memory_usage is None:
            memory_usage = get_option('display.memory_usage')
        if memory_usage:
            # append memory usage of df to display
            size_qualifier = ''
            if memory_usage == 'deep':
                deep = True
            else:
                # size_qualifier is just a best effort; not guaranteed to catch
                # all cases (e.g., it misses categorical data even with object
                # categories)
                deep = False
                if 'object' in counts or is_object_dtype(self.index):
                    size_qualifier = '+'
            mem_usage = self.memory_usage(index=True, deep=deep).sum()
            lines.append("memory usage: %s\n" %
                         _sizeof_fmt(mem_usage, size_qualifier))
        _put_lines(buf, lines)
