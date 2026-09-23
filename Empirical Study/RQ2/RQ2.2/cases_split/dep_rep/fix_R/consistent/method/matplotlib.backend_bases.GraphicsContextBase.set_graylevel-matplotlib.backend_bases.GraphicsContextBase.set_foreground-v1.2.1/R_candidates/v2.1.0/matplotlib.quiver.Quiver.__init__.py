    @docstring.Substitution(_quiver_doc)
    def __init__(self, ax, *args, **kw):
        """
        The constructor takes one required argument, an Axes
        instance, followed by the args and kwargs described
        by the following pylab interface documentation:
        %s
        """
        self.ax = ax
        X, Y, U, V, C = _parse_args(*args)
        self.X = X
        self.Y = Y
        self.XY = np.hstack((X[:, np.newaxis], Y[:, np.newaxis]))
        self.N = len(X)
        self.scale = kw.pop('scale', None)
        self.headwidth = kw.pop('headwidth', 3)
        self.headlength = float(kw.pop('headlength', 5))
        self.headaxislength = kw.pop('headaxislength', 4.5)
        self.minshaft = kw.pop('minshaft', 1)
        self.minlength = kw.pop('minlength', 1)
        self.units = kw.pop('units', 'width')
        self.scale_units = kw.pop('scale_units', None)
        self.angles = kw.pop('angles', 'uv')
        self.width = kw.pop('width', None)
        self.color = kw.pop('color', 'k')

        pivot = kw.pop('pivot', 'tail').lower()
        # validate pivot
        if pivot not in self._PIVOT_VALS:
            raise ValueError(
                'pivot must be one of {keys}, you passed {inp}'.format(
                      keys=self._PIVOT_VALS, inp=pivot))
        # normalize to 'middle'
        if pivot == 'mid':
            pivot = 'middle'
        self.pivot = pivot

        self.transform = kw.pop('transform', ax.transData)
        kw.setdefault('facecolors', self.color)
        kw.setdefault('linewidths', (0,))
        mcollections.PolyCollection.__init__(self, [], offsets=self.XY,
                                             transOffset=self.transform,
                                             closed=False,
                                             **kw)
        self.polykw = kw
        self.set_UVC(U, V, C)
        self._initialized = False

        self.keyvec = None
        self.keytext = None

        # try to prevent closure over the real self
        weak_self = weakref.ref(self)

        def on_dpi_change(fig):
            self_weakref = weak_self()
            if self_weakref is not None:
                self_weakref._new_UV = True  # vertices depend on width, span
                                             # which in turn depend on dpi
                self_weakref._initialized = False  # simple brute force update
                                                   # works because _init is
                                                   # called at the start of
                                                   # draw.

        self._cid = self.ax.figure.callbacks.connect('dpi_changed',
                                                     on_dpi_change)
