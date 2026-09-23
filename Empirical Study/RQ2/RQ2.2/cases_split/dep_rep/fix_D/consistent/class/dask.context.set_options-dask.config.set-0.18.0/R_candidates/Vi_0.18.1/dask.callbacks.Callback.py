class Callback(object):
    """ Base class for using the callback mechanism

    Create a callback with functions of the following signatures:

    >>> def start(dsk):
    ...     pass
    >>> def start_state(dsk, state):
    ...     pass
    >>> def pretask(key, dsk, state):
    ...     pass
    >>> def posttask(key, result, dsk, state, worker_id):
    ...     pass
    >>> def finish(dsk, state, failed):
    ...     pass

    You may then construct a callback object with any number of them

    >>> cb = Callback(pretask=pretask, finish=finish)  # doctest: +SKIP

    And use it either as a context manager over a compute/get call

    >>> with cb:  # doctest: +SKIP
    ...     x.compute()  # doctest: +SKIP

    Or globally with the ``register`` method

    >>> cb.register()  # doctest: +SKIP
    >>> cb.unregister()  # doctest: +SKIP

    Alternatively subclass the ``Callback`` class with your own methods.

    >>> class PrintKeys(Callback):
    ...     def _pretask(self, key, dask, state):
    ...         print("Computing: {0}!".format(repr(key)))

    >>> with PrintKeys():  # doctest: +SKIP
    ...     x.compute()  # doctest: +SKIP
    """
    active = set()

    def __init__(self, start=None, start_state=None, pretask=None, posttask=None, finish=None):
        if start:
            self._start = start
        if start_state:
            self._start_state = start_state
        if pretask:
            self._pretask = pretask
        if posttask:
            self._posttask = posttask
        if finish:
            self._finish = finish

    @property
    def _callback(self):
        fields = ['_start', '_start_state', '_pretask', '_posttask', '_finish']
        return tuple(getattr(self, i, None) for i in fields)

    def __enter__(self):
        self._cm = add_callbacks(self)
        self._cm.__enter__()
        return self

    def __exit__(self, *args):
        self._cm.__exit__(*args)

    def register(self):
        Callback.active.add(self._callback)

    def unregister(self):
        Callback.active.remove(self._callback)
