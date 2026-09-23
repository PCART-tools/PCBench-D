class FuncAnimation(TimedAnimation):
    """
    Makes an animation by repeatedly calling a function *func*.

    .. note::

        You must store the created Animation in a variable that lives as long
        as the animation should run. Otherwise, the Animation object will be
        garbage-collected and the animation stops.

    Parameters
    ----------
    fig : `~matplotlib.figure.Figure`
        The figure object used to get needed events, such as draw or resize.

    func : callable
        The function to call at each frame.  The first argument will
        be the next value in *frames*.   Any additional positional
        arguments can be supplied via the *fargs* parameter.

        The required signature is::

            def func(frame, *fargs) -> iterable_of_artists

        If ``blit == True``, *func* must return an iterable of all artists
        that were modified or created. This information is used by the blitting
        algorithm to determine which parts of the figure have to be updated.
        The return value is unused if ``blit == False`` and may be omitted in
        that case.

    frames : iterable, int, generator function, or None, optional
        Source of data to pass *func* and each frame of the animation

        - If an iterable, then simply use the values provided.  If the
          iterable has a length, it will override the *save_count* kwarg.

        - If an integer, then equivalent to passing ``range(frames)``

        - If a generator function, then must have the signature::

             def gen_function() -> obj

        - If *None*, then equivalent to passing ``itertools.count``.

        In all of these cases, the values in *frames* is simply passed through
        to the user-supplied *func* and thus can be of any type.

    init_func : callable, optional
        A function used to draw a clear frame. If not given, the results of
        drawing from the first item in the frames sequence will be used. This
        function will be called once before the first frame.

        The required signature is::

            def init_func() -> iterable_of_artists

        If ``blit == True``, *init_func* must return an iterable of artists
        to be re-drawn. This information is used by the blitting algorithm to
        determine which parts of the figure have to be updated.  The return
        value is unused if ``blit == False`` and may be omitted in that case.

    fargs : tuple or None, optional
        Additional arguments to pass to each call to *func*.

    save_count : int, default: 100
        Fallback for the number of values from *frames* to cache. This is
        only used if the number of frames cannot be inferred from *frames*,
        i.e. when it's an iterator without length or a generator.

    interval : int, default: 200
        Delay between frames in milliseconds.

    repeat_delay : int, default: 0
        The delay in milliseconds between consecutive animation runs, if
        *repeat* is True.

    repeat : bool, default: True
        Whether the animation repeats when the sequence of frames is completed.

    blit : bool, default: False
        Whether blitting is used to optimize drawing.  Note: when using
        blitting, any animated artists will be drawn according to their zorder;
        however, they will be drawn on top of any previous artists, regardless
        of their zorder.

    cache_frame_data : bool, default: True
        Whether frame data is cached.  Disabling cache might be helpful when
        frames contain large objects.
    """

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
            if kwargs.get('repeat', True):
                self._tee_from = frames
                def iter_frames(frames=frames):
                    this, self._tee_from = itertools.tee(self._tee_from, 2)
                    yield from this
                self._iter_gen = iter_frames
            else:
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
            # of a native python int (https://bugs.python.org/issue30537).
            # As a workaround, convert save_count to a native python int.
            self.save_count = int(self.save_count)

        self._cache_frame_data = cache_frame_data

        # Needs to be initialized so the draw functions work without checking
        self._save_seq = []

        super().__init__(fig, **kwargs)

        # Need to reset the saved seq, since right now it will contain data
        # for a single frame from init, which is not what we want.
        self._save_seq = []

    def new_frame_seq(self):
        # Use the generating function to generate a new frame sequence
        return self._iter_gen()

    def new_saved_frame_seq(self):
        # Generate an iterator for the sequence of saved data. If there are
        # no saved frames, generate a new frame sequence and take the first
        # save_count entries in it.
        if self._save_seq:
            # While iterating we are going to update _save_seq
            # so make a copy to safely iterate over
            self._old_saved_seq = list(self._save_seq)
            return iter(self._old_saved_seq)
        else:
            if self.save_count is not None:
                return itertools.islice(self.new_frame_seq(), self.save_count)

            else:
                frame_seq = self.new_frame_seq()

                def gen():
                    try:
                        for _ in range(100):
                            yield next(frame_seq)
                    except StopIteration:
                        pass
                    else:
                        _api.warn_deprecated(
                            "2.2", message="FuncAnimation.save has truncated "
                            "your animation to 100 frames.  In the future, no "
                            "such truncation will occur; please pass "
                            "'save_count' accordingly.")

                return gen()

    def _init_draw(self):
        super()._init_draw()
        # Initialize the drawing either using the given init_func or by
        # calling the draw function with the first item of the frame sequence.
        # For blitting, the init_func should return a sequence of modified
        # artists.
        if self._init_func is None:
            try:
                frame_data = next(self.new_frame_seq())
            except StopIteration:
                # we can't start the iteration, it may have already been
                # exhausted by a previous save or just be 0 length.
                # warn and bail.
                warnings.warn(
                    "Can not start iterating the frames for the initial draw. "
                    "This can be caused by passing in a 0 length sequence "
                    "for *frames*.\n\n"
                    "If you passed *frames* as a generator "
                    "it may be exhausted due to a previous display or save."
                )
                return
            self._draw_frame(frame_data)
        else:
            self._drawn_artists = self._init_func()
            if self._blit:
                if self._drawn_artists is None:
                    raise RuntimeError('The init_func must return a '
                                       'sequence of Artist objects.')
                for a in self._drawn_artists:
                    a.set_animated(self._blit)
        self._save_seq = []

    def _draw_frame(self, framedata):
        if self._cache_frame_data:
            # Save the data for potential saving of movies.
            self._save_seq.append(framedata)

        # Make sure to respect save_count (keep only the last save_count
        # around)
        self._save_seq = self._save_seq[-self.save_count:]

        # Call the func with framedata and args. If blitting is desired,
        # func needs to return a sequence of any artists that were modified.
        self._drawn_artists = self._func(framedata, *self._args)

        if self._blit:

            err = RuntimeError('The animation function must return a sequence '
                               'of Artist objects.')
            try:
                # check if a sequence
                iter(self._drawn_artists)
            except TypeError:
                raise err from None

            # check each item if it's artist
            for i in self._drawn_artists:
                if not isinstance(i, mpl.artist.Artist):
                    raise err

            self._drawn_artists = sorted(self._drawn_artists,
                                         key=lambda x: x.get_zorder())

            for a in self._drawn_artists:
                a.set_animated(self._blit)
