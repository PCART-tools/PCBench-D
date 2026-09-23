class ResourceProfiler(Callback):
    """A profiler for resource use.

    Records the following each timestep
        1. Time in seconds since the epoch
        2. Memory usage in MB
        3. % CPU usage

    Examples
    --------

    >>> from operator import add, mul
    >>> from dask.threaded import get
    >>> dsk = {'x': 1, 'y': (add, 'x', 10), 'z': (mul, 'y', 2)}
    >>> with ResourceProfiler() as prof:  # doctest: +SKIP
    ...     get(dsk, 'z')
    22

    These results can be visualized in a bokeh plot using the ``visualize``
    method. Note that this requires bokeh to be installed.

    >>> prof.visualize() # doctest: +SKIP

    You can activate the profiler globally

    >>> prof.register()  # doctest: +SKIP

    If you use the profiler globally you will need to clear out old results
    manually.

    >>> prof.clear()  # doctest: +SKIP

    Note that when used as a context manager data will be collected throughout
    the duration of the enclosed block. In contrast, when registered globally
    data will only be collected while a dask scheduler is active.
    """
    def __init__(self, dt=1):
        self._dt = dt
        self._entered = False
        self._tracker = None
        self.results = []

    def _is_running(self):
        return self._tracker is not None and self._tracker.is_alive()

    def _start_collect(self):
        if not self._is_running():
            self._tracker = _Tracker(self._dt)
            self._tracker.start()
        self._tracker.parent_conn.send('collect')

    def _stop_collect(self):
        if self._is_running():
            self._tracker.parent_conn.send('send_data')
            self.results.extend(starmap(ResourceData, self._tracker.parent_conn.recv()))

    def __enter__(self):
        self._entered = True
        self.clear()
        self._start_collect()
        return super(ResourceProfiler, self).__enter__()

    def __exit__(self, *args):
        self._entered = False
        self._stop_collect()
        self.close()
        super(ResourceProfiler, self).__exit__(*args)

    def _start(self, dsk):
        self._start_collect()

    def _finish(self, dsk, state, failed):
        if not self._entered:
            self._stop_collect()

    def close(self):
        """Shutdown the resource tracker process"""
        if self._is_running():
            self._tracker.shutdown()
            self._tracker = None

    __del__ = close

    def clear(self):
        self.results = []

    def _plot(self, **kwargs):
        from .profile_visualize import plot_resources
        return plot_resources(self.results, **kwargs)

    def visualize(self, **kwargs):
        """Visualize the profiling run in a bokeh plot.

        See also
        --------
        dask.diagnostics.profile_visualize.visualize
        """
        from .profile_visualize import visualize
        return visualize(self, **kwargs)
