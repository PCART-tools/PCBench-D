class CacheProfiler(Callback):
    """A profiler for dask execution at the scheduler cache level.

    Records the following information for each task:
        1. Key
        2. Task
        3. Size metric
        4. Cache entry time in seconds since the epoch
        5. Cache exit time in seconds since the epoch

    Examples
    --------

    >>> from operator import add, mul
    >>> from dask.threaded import get
    >>> dsk = {'x': 1, 'y': (add, 'x', 10), 'z': (mul, 'y', 2)}
    >>> with CacheProfiler() as prof:
    ...     get(dsk, 'z')
    22

    >>> prof.results    # doctest: +SKIP
    [CacheData('y', (add, 'x', 10), 1, 1435352238.48039, 1435352238.480655),
     CacheData('z', (mul, 'y', 2), 1, 1435352238.480657, 1435352238.480803)]

    The default is to count each task (``metric`` is 1 for all tasks). Other
    functions may used as a metric instead through the ``metric`` keyword. For
    example, the ``nbytes`` function found in ``cachey`` can be used to measure
    the number of bytes in the cache.

    >>> from cachey import nbytes    # doctest: +SKIP
    >>> with CacheProfiler(metric=nbytes) as prof:  # doctest: +SKIP
    ...     get(dsk, 'z')

    The profiling results can be visualized in a bokeh plot using the
    ``visualize`` method. Note that this requires bokeh to be installed.

    >>> prof.visualize() # doctest: +SKIP

    You can activate the profiler globally

    >>> prof.register()  # doctest: +SKIP

    If you use the profiler globally you will need to clear out old results
    manually.

    >>> prof.clear()

    """

    def __init__(self, metric=None, metric_name=None):
        self.clear()
        self._metric = metric if metric else lambda value: 1
        if metric_name:
            self._metric_name = metric_name
        elif metric:
            self._metric_name = metric.__name__
        else:
            self._metric_name = 'count'

    def __enter__(self):
        self.clear()
        return super(CacheProfiler, self).__enter__()

    def _start(self, dsk):
        self._dsk.update(dsk)
        if not self._start_time:
            self._start_time = default_timer()

    def _posttask(self, key, value, dsk, state, id):
        t = default_timer()
        self._cache[key] = (self._metric(value), t)
        for k in state['released'].intersection(self._cache):
            metric, start = self._cache.pop(k)
            self.results.append(CacheData(k, dsk[k], metric, start, t))

    def _finish(self, dsk, state, failed):
        t = default_timer()
        for k, (metric, start) in self._cache.items():
            self.results.append(CacheData(k, dsk[k], metric, start, t))
        self._cache.clear()

    def _plot(self, **kwargs):
        from .profile_visualize import plot_cache
        return plot_cache(self.results, self._dsk, self._start_time,
                          self._metric_name, **kwargs)

    def visualize(self, **kwargs):
        """Visualize the profiling run in a bokeh plot.

        See also
        --------
        dask.diagnostics.profile_visualize.visualize
        """
        from .profile_visualize import visualize
        return visualize(self, **kwargs)

    def clear(self):
        """Clear out old results from profiler"""
        self.results = []
        self._cache = {}
        self._dsk = {}
        self._start_time = None
