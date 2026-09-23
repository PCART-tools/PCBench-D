    @Appender(_shared_docs['describe'] % _shared_doc_kwargs)
    def describe(self, percentile_width=None, percentiles=None, include=None, exclude=None ):
        if self.ndim >= 3:
            msg = "describe is not implemented on on Panel or PanelND objects."
            raise NotImplementedError(msg)

        if percentile_width is not None and percentiles is not None:
            msg = "Cannot specify both 'percentile_width' and 'percentiles.'"
            raise ValueError(msg)
        if percentiles is not None:
            # get them all to be in [0, 1]
            percentiles = np.asarray(percentiles)
            if (percentiles > 1).any():
                percentiles = percentiles / 100.0
                msg = ("percentiles should all be in the interval [0, 1]. "
                       "Try {0} instead.")
                raise ValueError(msg.format(list(percentiles)))
        else:
            # only warn if they change the default
            if percentile_width is not None:
                do_warn = True
            else:
                do_warn = False
            percentile_width = percentile_width or 50
            lb = .5 * (1. - percentile_width / 100.)
            ub = 1. - lb
            percentiles = np.array([lb, 0.5, ub])
            if do_warn:
                msg = ("The `percentile_width` keyword is deprecated. "
                       "Use percentiles={0} instead".format(list(percentiles)))
                warnings.warn(msg, FutureWarning)

        # median should always be included
        if (percentiles != 0.5).all():  # median isn't included
            lh = percentiles[percentiles < .5]
            uh = percentiles[percentiles > .5]
            percentiles = np.hstack([lh, 0.5, uh])

        def pretty_name(x):
            x *= 100
            if x == int(x):
                return '%.0f%%' % x
            else:
                return '%.1f%%' % x

        def describe_numeric_1d(series, percentiles):
            stat_index = (['count', 'mean', 'std', 'min'] +
                  [pretty_name(x) for x in percentiles] + ['max'])
            d = ([series.count(), series.mean(), series.std(), series.min()] +
                 [series.quantile(x) for x in percentiles] + [series.max()])
            return pd.Series(d, index=stat_index, name=series.name)


        def describe_categorical_1d(data):
            names = ['count', 'unique']
            objcounts = data.value_counts()
            result = [data.count(), len(objcounts[objcounts!=0])]
            if result[1] > 0:
                top, freq = objcounts.index[0], objcounts.iloc[0]

                if data.dtype == object or com.is_categorical_dtype(data.dtype):
                    names += ['top', 'freq']
                    result += [top, freq]

                elif com.is_datetime64_dtype(data):
                    asint = data.dropna().values.view('i8')
                    names += ['top', 'freq', 'first', 'last']
                    result += [lib.Timestamp(top), freq,
                               lib.Timestamp(asint.min()),
                               lib.Timestamp(asint.max())]

            return pd.Series(result, index=names, name=data.name)

        def describe_1d(data, percentiles):
            if com.is_numeric_dtype(data):
                return describe_numeric_1d(data, percentiles)
            elif com.is_timedelta64_dtype(data):
                return describe_numeric_1d(data, percentiles)
            else:
                return describe_categorical_1d(data)

        if self.ndim == 1:
            return describe_1d(self, percentiles)
        elif (include is None) and (exclude is None):
            if len(self._get_numeric_data()._info_axis) > 0:
                # when some numerics are found, keep only numerics
                data = self.select_dtypes(include=[np.number, np.bool])
            else:
                data = self
        elif include == 'all':
            if exclude != None:
                msg = "exclude must be None when include is 'all'"
                raise ValueError(msg)
            data = self
        else:
            data = self.select_dtypes(include=include, exclude=exclude)

        ldesc = [describe_1d(s, percentiles) for _, s in data.iteritems()]
        # set a convenient order for rows
        names = []
        ldesc_indexes = sorted([x.index for x in ldesc], key=len)
        for idxnames in ldesc_indexes:
            for name in idxnames:
                if name not in names:
                    names.append(name)
        d = pd.concat(ldesc, join_axes=pd.Index([names]), axis=1)
        return d
