    def _helper_csv(self, writer, na_rep=None, cols=None,
                    header=True, index=True,
                    index_label=None, float_format=None, date_format=None):
        if cols is None:
            cols = self.columns

        has_aliases = isinstance(header, (tuple, list, np.ndarray, Index))
        if has_aliases or header:
            if index:
                # should write something for index label
                if index_label is not False:
                    if index_label is None:
                        if isinstance(self.obj.index, MultiIndex):
                            index_label = []
                            for i, name in enumerate(self.obj.index.names):
                                if name is None:
                                    name = ''
                                index_label.append(name)
                        else:
                            index_label = self.obj.index.name
                            if index_label is None:
                                index_label = ['']
                            else:
                                index_label = [index_label]
                    elif not isinstance(index_label,
                                        (list, tuple, np.ndarray, Index)):
                        # given a string for a DF with Index
                        index_label = [index_label]

                    encoded_labels = list(index_label)
                else:
                    encoded_labels = []

                if has_aliases:
                    if len(header) != len(cols):
                        raise ValueError(('Writing %d cols but got %d aliases'
                                          % (len(cols), len(header))))
                    else:
                        write_cols = header
                else:
                    write_cols = cols
                encoded_cols = list(write_cols)

                writer.writerow(encoded_labels + encoded_cols)
            else:
                encoded_cols = list(cols)
                writer.writerow(encoded_cols)

        if date_format is None:
            date_formatter = lambda x: Timestamp(x)._repr_base
        else:
            def strftime_with_nulls(x):
                x = Timestamp(x)
                if notnull(x):
                    return x.strftime(date_format)

            date_formatter = lambda x: strftime_with_nulls(x)

        data_index = self.obj.index

        if isinstance(self.obj.index, PeriodIndex):
            data_index = self.obj.index.to_timestamp()

        if isinstance(data_index, DatetimeIndex) and date_format is not None:
            data_index = Index([date_formatter(x) for x in data_index])

        values = self.obj.copy()
        values.index = data_index
        values.columns = values.columns.to_native_types(
            na_rep=na_rep,
            float_format=float_format,
            date_format=date_format,
            quoting=self.quoting)
        values = values[cols]

        series = {}
        for k, v in compat.iteritems(values._series):
            series[k] = v.values

        nlevels = getattr(data_index, 'nlevels', 1)
        for j, idx in enumerate(data_index):
            row_fields = []
            if index:
                if nlevels == 1:
                    row_fields = [idx]
                else:  # handle MultiIndex
                    row_fields = list(idx)
            for i, col in enumerate(cols):
                val = series[col][j]
                if lib.checknull(val):
                    val = na_rep

                if float_format is not None and com.is_float(val):
                    val = float_format % val
                elif isinstance(val, (np.datetime64, Timestamp)):
                    val = date_formatter(val)

                row_fields.append(val)

            writer.writerow(row_fields)
