    @docstring.Substitution(_quiver_doc)
    def __init__(self, ax, *args,
                 scale=None, headwidth=3, headlength=5, headaxislength=4.5,
                 minshaft=1, minlength=1, units='width', scale_units=None,
                 angles='uv', width=None, color='k', pivot='tail', **kw):
        """
        The constructor takes one required argument, an Axes
        instance, followed by the args and kwargs described
        by the following pyplot interface documentation:
        %s
        """
        self.ax = ax
        X, Y, U, V, C = _parse_args(*args)
        self.X = X
        self.Y = Y
        self.XY = np.column_stack((X, Y))
        self.N = len(X)
        self.scale = scale
        self.headwidth = headwidth
        self.headlength = float(headlength)
        self.headaxislength = headaxislength
        self.minshaft = minshaft
        self.minlength = minlength
        self.units = units
        self.scale_units = scale_units
        self.angles = angles
        self.width = width
        self.color = color

        if pivot.lower() == 'mid':
            pivot = 'middle'
        self.pivot = pivot.lower()
        if self.pivot not in self._PIVOT_VALS:
            raise ValueError(
                'pivot must be one of {keys}, you passed {inp}'.format(
                      keys=self._PIVOT_VALS, inp=pivot))

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
