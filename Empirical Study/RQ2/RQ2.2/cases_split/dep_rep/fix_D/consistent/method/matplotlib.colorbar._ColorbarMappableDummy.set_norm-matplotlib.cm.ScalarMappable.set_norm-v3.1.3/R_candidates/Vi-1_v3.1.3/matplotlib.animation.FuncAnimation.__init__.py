    def __init__(self, fig, func, frames=None, init_func=None, fargs=None,
                 save_count=None, *, cache_frame_data=True, **kwargs):
        if fargs:
            self._args = fargs
        else:
            self._args = ()
        self._func = func
        self._init_func = init_func

        # Amount of framedata to keep around for saving movies. This is only
        # used if we don't know how many frames there will be: in the case
        # of no generator or in the case of a callable.
        self.save_count = save_count
        # Set up a function that creates a new iterable when needed. If nothing
        # is passed in for frames, just use itertools.count, which will just
        # keep counting from 0. A callable passed in for frames is assumed to
        # be a generator. An iterable will be used as is, and anything else
        # will be treated as a number of frames.
        if frames is None:
            self._iter_gen = itertools.count
        elif callable(frames):
            self._iter_gen = frames
        elif np.iterable(frames):
            self._iter_gen = lambda: iter(frames)
            if hasattr(frames, '__len__'):
                self.save_count = len(frames)
        else:
            self._iter_gen = lambda: iter(range(frames))
            self.save_count = frames

        if self.save_count is None:
            # If we're passed in and using the default, set save_count to 100.
            self.save_count = 100
        else:
            # itertools.islice returns an error when passed a numpy int instead
            # of a native python int (http://bugs.python.org/issue30537).
            # As a workaround, convert save_count to a native python int.
            self.save_count = int(self.save_count)

        self._cache_frame_data = cache_frame_data

        # Needs to be initialized so the draw functions work without checking
        self._save_seq = []

        TimedAnimation.__init__(self, fig, **kwargs)

        # Need to reset the saved seq, since right now it will contain data
        # for a single frame from init, which is not what we want.
        self._save_seq = []
