    @Appender(_shared_docs['describe'] % _shared_doc_kwargs)
    def describe(self, percentiles=None, include=None, exclude=None):
        if self.ndim >= 3:
            msg = "describe is not implemented on Panel or PanelND objects."
            raise NotImplementedError(msg)
        elif self.ndim == 2 and self.columns.size == 0:
            raise ValueError("Cannot describe a DataFrame without columns")

        if percentiles is not None:
            # get them all to be in [0, 1]
            self._check_percentile(percentiles)

            # median should always be included
            if 0.5 not in percentiles:
                percentiles.append(0.5)
            percentiles = np.asarray(percentiles)
        else:
            percentiles = np.array([0.25, 0.5, 0.75])

        # sort and check for duplicates
        unique_pcts = np.unique(percentiles)
        if len(unique_pcts) < len(percentiles):
            raise ValueError("percentiles cannot contain duplicates")
        percentiles = unique_pcts

        formatted_percentiles = format_percentiles(percentiles)

        def describe_numeric_1d(series):
            stat_index = (['count', 'mean', 'std', 'min'] +
                          formatted_percentiles + ['max'])
            d = ([series.count(), series.mean(), series.std(), series.min()] +
                 [series.quantile(x) for x in percentiles] + [series.max()])
            return pd.Series(d, index=stat_index, name=series.name)

        def describe_categorical_1d(data):
            names = ['count', 'unique']
            objcounts = data.value_counts()
            count_unique = len(objcounts[objcounts != 0])
            result = [data.count(), count_unique]
            if result[1] > 0:
                top, freq = objcounts.index[0], objcounts.iloc[0]

                if is_datetime64_dtype(data):
                    asint = data.dropna().values.view('i8')
                    names += ['top', 'freq', 'first', 'last']
                    result += [lib.Timestamp(top), freq,
                               lib.Timestamp(asint.min()),
                               lib.Timestamp(asint.max())]
                else:
                    names += ['top', 'freq']
                    result += [top, freq]

            return pd.Series(result, index=names, name=data.name)

        def describe_1d(data):
            if is_bool_dtype(data):
                return describe_categorical_1d(data)
            elif is_numeric_dtype(data):
                return describe_numeric_1d(data)
            elif is_timedelta64_dtype(data):
                return describe_numeric_1d(data)
            else:
                return describe_categorical_1d(data)

        if self.ndim == 1:
            return describe_1d(self)
        elif (include is None) and (exclude is None):
            # when some numerics are found, keep only numerics
            data = self.select_dtypes(include=[np.number])
            if len(data.columns) == 0:
                data = self
        elif include == 'all':
            if exclude is not None:
                msg = "exclude must be None when include is 'all'"
                raise ValueError(msg)
            data = self
        else:
            data = self.select_dtypes(include=include, exclude=exclude)

        ldesc = [describe_1d(s) for _, s in data.iteritems()]
        # set a convenient order for rows
        names = []
        ldesc_indexes = sorted([x.index for x in ldesc], key=len)
        for idxnames in ldesc_indexes:
            for name in idxnames:
                if name not in names:
                    names.append(name)

        d = pd.concat(ldesc, join_axes=pd.Index([names]), axis=1)
        d.columns = data.columns.copy()
        return d
