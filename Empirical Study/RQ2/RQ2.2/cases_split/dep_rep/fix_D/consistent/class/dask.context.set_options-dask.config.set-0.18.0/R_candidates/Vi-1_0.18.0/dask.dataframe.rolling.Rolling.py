class Rolling(object):
    """Provides rolling window calculations."""

    def __init__(self, obj, window=None, min_periods=None, freq=None,
                 center=False, win_type=None, axis=0):
        if freq is not None:
            msg = 'The deprecated freq argument is not supported.'
            raise NotImplementedError(msg)

        self.obj = obj     # dataframe or series
        self.window = window
        self.min_periods = min_periods
        self.center = center
        self.axis = axis
        self.win_type = win_type
        # Allow pandas to raise if appropriate
        pd_roll = obj._meta.rolling(**self._rolling_kwargs())
        # Using .rolling(window='2s'), pandas will convert the
        # offset str to a window in nanoseconds. But pandas doesn't
        # accept the integer window with win_type='freq', so we store
        # that information here.
        # See https://github.com/pandas-dev/pandas/issues/15969
        self._window = pd_roll.window
        self._win_type = pd_roll.win_type
        self._min_periods = pd_roll.min_periods

    def _rolling_kwargs(self):
        return {'window': self.window,
                'min_periods': self.min_periods,
                'center': self.center,
                'win_type': self.win_type,
                'axis': self.axis}

    @property
    def _has_single_partition(self):
        """
        Indicator for whether the object has a single partition (True)
        or multiple (False).
        """
        return (self.axis in (1, 'columns') or
                (isinstance(self.window, int) and self.window <= 1) or
                self.obj.npartitions == 1)

    def _call_method(self, method_name, *args, **kwargs):
        rolling_kwargs = self._rolling_kwargs()
        meta = pandas_rolling_method(self.obj._meta_nonempty, rolling_kwargs,
                                     method_name, *args, **kwargs)

        if self._has_single_partition:
            # There's no overlap just use map_partitions
            return self.obj.map_partitions(pandas_rolling_method,
                                           rolling_kwargs, method_name,
                                           *args, token=method_name, meta=meta,
                                           **kwargs)
        # Convert window to overlap
        if self.center:
            before = self.window // 2
            after = self.window - before - 1
        elif self._win_type == 'freq':
            before = pd.Timedelta(self.window)
            after = 0
        else:
            before = self.window - 1
            after = 0
        return map_overlap(pandas_rolling_method, self.obj, before, after,
                           rolling_kwargs, method_name, *args,
                           token=method_name, meta=meta, **kwargs)

    @derived_from(pd_Rolling)
    def count(self):
        return self._call_method('count')

    @derived_from(pd_Rolling)
    def sum(self):
        return self._call_method('sum')

    @derived_from(pd_Rolling)
    def mean(self):
        return self._call_method('mean')

    @derived_from(pd_Rolling)
    def median(self):
        return self._call_method('median')

    @derived_from(pd_Rolling)
    def min(self):
        return self._call_method('min')

    @derived_from(pd_Rolling)
    def max(self):
        return self._call_method('max')

    @derived_from(pd_Rolling)
    def std(self, ddof=1):
        return self._call_method('std', ddof=1)

    @derived_from(pd_Rolling)
    def var(self, ddof=1):
        return self._call_method('var', ddof=1)

    @derived_from(pd_Rolling)
    def skew(self):
        return self._call_method('skew')

    @derived_from(pd_Rolling)
    def kurt(self):
        return self._call_method('kurt')

    @derived_from(pd_Rolling)
    def quantile(self, quantile):
        return self._call_method('quantile', quantile)

    @derived_from(pd_Rolling)
    def apply(self, func, args=(), kwargs={}, **kwds):
        # TODO: In a future version of pandas this will change to
        # raw=False. Think about inspecting the function signature and setting
        # to that?
        if PANDAS_VERSION >= '0.23.0':
            kwds.setdefault("raw", None)
        else:
            if kwargs:
                msg = ("Invalid argument to 'apply'. Keyword arguments "
                       "should be given as a dict to the 'kwargs' arugment. ")
                raise TypeError(msg)
        return self._call_method('apply', func, args=args,
                                 kwargs=kwargs, **kwds)

    def __repr__(self):

        def order(item):
            k, v = item
            _order = {'window': 0, 'min_periods': 1, 'center': 2,
                      'win_type': 3, 'axis': 4}
            return _order[k]

        rolling_kwargs = self._rolling_kwargs()
        # pandas translates the '2S' offset to nanoseconds
        rolling_kwargs['window'] = self._window
        rolling_kwargs['win_type'] = self._win_type
        return 'Rolling [{}]'.format(','.join(
            '{}={}'.format(k, v)
            for k, v in sorted(rolling_kwargs.items(), key=order)
            if v is not None))
