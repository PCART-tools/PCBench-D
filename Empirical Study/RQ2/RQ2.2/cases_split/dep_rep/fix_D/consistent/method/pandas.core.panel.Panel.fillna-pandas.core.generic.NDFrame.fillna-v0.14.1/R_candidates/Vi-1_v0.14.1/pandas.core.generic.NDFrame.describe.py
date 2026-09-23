    @Appender(_shared_docs['describe'] % _shared_doc_kwargs)
    def describe(self, percentile_width=None, percentiles=None):
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

        # dtypes: numeric only, numeric mixed, objects only
        data = self._get_numeric_data()
        if self.ndim > 1:
            if len(data._info_axis) == 0:
                is_object = True
            else:
                is_object = False
        else:
            is_object = not self._is_numeric_mixed_type

        def pretty_name(x):
            x *= 100
            if x == int(x):
                return '%.0f%%' % x
            else:
                return '%.1f%%' % x

        def describe_numeric_1d(series, percentiles):
            return ([series.count(), series.mean(), series.std(),
                     series.min()] +
                    [series.quantile(x) for x in percentiles] +
                    [series.max()])

        def describe_categorical_1d(data):
            names = ['count', 'unique']
            objcounts = data.value_counts()
            result = [data.count(), len(objcounts)]
            if result[1] > 0:
                top, freq = objcounts.index[0], objcounts.iloc[0]

                if data.dtype == object:
                    names += ['top', 'freq']
                    result += [top, freq]

                elif issubclass(data.dtype.type, np.datetime64):
                    asint = data.dropna().values.view('i8')
                    names += ['first', 'last', 'top', 'freq']
                    result += [lib.Timestamp(asint.min()),
                               lib.Timestamp(asint.max()),
                               lib.Timestamp(top), freq]

            return pd.Series(result, index=names)

        if is_object:
            if data.ndim == 1:
                return describe_categorical_1d(self)
            else:
                result = pd.DataFrame(dict((k, describe_categorical_1d(v))
                                           for k, v in compat.iteritems(self)),
                                      columns=self._info_axis,
                                      index=['count', 'unique', 'first', 'last',
                                             'top', 'freq'])
                # just objects, no datime
                if pd.isnull(result.loc['first']).all():
                    result = result.drop(['first', 'last'], axis=0)
                return result
        else:
            stat_index = (['count', 'mean', 'std', 'min'] +
                          [pretty_name(x) for x in percentiles] +
                          ['max'])
            if data.ndim == 1:
                return pd.Series(describe_numeric_1d(data, percentiles),
                                 index=stat_index)
            else:
                destat = []
                for i in range(len(data._info_axis)):  # BAD
                    series = data.iloc[:, i]
                    destat.append(describe_numeric_1d(series, percentiles))

                return self._constructor(lmap(list, zip(*destat)),
                                         index=stat_index,
                                         columns=data._info_axis)
