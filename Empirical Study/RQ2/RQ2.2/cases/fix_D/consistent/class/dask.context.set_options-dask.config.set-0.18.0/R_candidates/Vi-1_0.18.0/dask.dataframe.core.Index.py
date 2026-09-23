class Index(Series):

    _partition_type = pd.Index
    _token_prefix = 'index-'

    _dt_attributes = {'nanosecond', 'microsecond', 'millisecond', 'dayofyear',
                      'minute', 'hour', 'day', 'dayofweek', 'second', 'week',
                      'weekday', 'weekofyear', 'month', 'quarter', 'year'}

    _cat_attributes = {'known', 'as_known', 'as_unknown', 'add_categories',
                       'categories', 'remove_categories', 'reorder_categories',
                       'as_ordered', 'codes', 'remove_unused_categories',
                       'set_categories', 'as_unordered', 'ordered',
                       'rename_categories'}

    def __getattr__(self, key):
        if is_categorical_dtype(self.dtype) and key in self._cat_attributes:
            return getattr(self.cat, key)
        elif key in self._dt_attributes:
            return getattr(self.dt, key)
        raise AttributeError("'Index' object has no attribute %r" % key)

    def __dir__(self):
        out = super(Index, self).__dir__()
        out.extend(self._dt_attributes)
        if is_categorical_dtype(self.dtype):
            out.extend(self._cat_attributes)
        return out

    @property
    def index(self):
        msg = "'{0}' object has no attribute 'index'"
        raise AttributeError(msg.format(self.__class__.__name__))

    def __array_wrap__(self, array, context=None):
        return pd.Index(array, name=self.name)

    def head(self, n=5, compute=True):
        """ First n items of the Index.

        Caveat, this only checks the first partition.
        """
        name = 'head-%d-%s' % (n, self._name)
        dsk = {(name, 0): (operator.getitem, (self._name, 0), slice(0, n))}

        result = new_dd_object(merge(self.dask, dsk), name,
                               self._meta, self.divisions[:2])

        if compute:
            result = result.compute()
        return result

    @derived_from(pd.Index)
    def max(self, split_every=False):
        return self.reduction(M.max, meta=self._meta_nonempty.max(),
                              token=self._token_prefix + 'max',
                              split_every=split_every)

    @derived_from(pd.Index)
    def min(self, split_every=False):
        return self.reduction(M.min, meta=self._meta_nonempty.min(),
                              token=self._token_prefix + 'min',
                              split_every=split_every)

    def count(self, split_every=False):
        return self.reduction(methods.index_count, np.sum,
                              token='index-count', meta=int,
                              split_every=split_every)

    @derived_from(pd.Index)
    def shift(self, periods=1, freq=None):
        if isinstance(self._meta, pd.PeriodIndex):
            if freq is not None:
                raise ValueError("PeriodIndex doesn't accept `freq` argument")
            meta = self._meta_nonempty.shift(periods)
            out = self.map_partitions(M.shift, periods, meta=meta,
                                      token='shift')
        else:
            # Pandas will raise for other index types that don't implement shift
            meta = self._meta_nonempty.shift(periods, freq=freq)
            out = self.map_partitions(M.shift, periods, token='shift',
                                      meta=meta, freq=freq)
        if freq is None:
            freq = meta.freq
        return maybe_shift_divisions(out, periods, freq=freq)
