class Resampler(object):
    def __init__(self, obj, rule, **kwargs):
        if not obj.known_divisions:
            msg = ("Can only resample dataframes with known divisions\n"
                   "See dask.pydata.org/en/latest/dataframe-design.html#partitions\n"
                   "for more information.")
            raise ValueError(msg)
        self.obj = obj
        rule = pd.tseries.frequencies.to_offset(rule)
        day_nanos = pd.tseries.frequencies.Day().nanos

        if getnanos(rule) and day_nanos % rule.nanos:
            raise NotImplementedError('Resampling frequency %s that does'
                                      ' not evenly divide a day is not '
                                      'implemented' % rule)
        self._rule = rule
        self._kwargs = kwargs

    def _agg(self, how, meta=None, fill_value=np.nan, how_args=(), how_kwargs={}):
        rule = self._rule
        kwargs = self._kwargs
        name = 'resample-' + tokenize(self.obj, rule, kwargs, how, *how_args,
                                      **how_kwargs)

        # Create a grouper to determine closed and label conventions
        newdivs, outdivs = _resample_bin_and_out_divs(self.obj.divisions, rule,
                                                      **kwargs)

        # Repartition divs into bins. These won't match labels after mapping
        partitioned = self.obj.repartition(newdivs, force=True)

        keys = partitioned.__dask_keys__()
        dsk = partitioned.dask

        args = zip(keys, outdivs, outdivs[1:], ['left'] * (len(keys) - 1) + [None])
        for i, (k, s, e, c) in enumerate(args):
            dsk[(name, i)] = (_resample_series, k, s, e, c,
                              rule, kwargs, how, fill_value, list(how_args),
                              how_kwargs)

        # Infer output metadata
        meta_r = self.obj._meta_nonempty.resample(self._rule, **self._kwargs)
        meta = getattr(meta_r, how)(*how_args, **how_kwargs)

        if isinstance(meta, pd.DataFrame):
            return DataFrame(dsk, name, meta, outdivs)
        return Series(dsk, name, meta, outdivs)

    @derived_from(pd_Resampler)
    def agg(self, agg_funcs, *args, **kwargs):
        return self._agg('agg', how_args=(agg_funcs,) + args, how_kwargs=kwargs)

    @derived_from(pd_Resampler)
    def count(self):
        return self._agg('count', fill_value=0)

    @derived_from(pd_Resampler)
    def first(self):
        return self._agg('first')

    @derived_from(pd_Resampler)
    def last(self):
        return self._agg('last')

    @derived_from(pd_Resampler)
    def mean(self):
        return self._agg('mean')

    @derived_from(pd_Resampler)
    def min(self):
        return self._agg('min')

    @derived_from(pd_Resampler)
    def median(self):
        return self._agg('median')

    @derived_from(pd_Resampler)
    def max(self):
        return self._agg('max')

    @derived_from(pd_Resampler)
    def ohlc(self):
        return self._agg('ohlc')

    @derived_from(pd_Resampler)
    def prod(self):
        return self._agg('prod')

    @derived_from(pd_Resampler)
    def sem(self):
        return self._agg('sem')

    @derived_from(pd_Resampler)
    def std(self):
        return self._agg('std')

    @derived_from(pd_Resampler)
    def sum(self):
        return self._agg('sum')

    @derived_from(pd_Resampler)
    def var(self):
        return self._agg('var')
