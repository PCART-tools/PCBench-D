    @docstring.interpd
    def __init__(self, ax, *args,
                 pivot='tip', length=7, barbcolor=None, flagcolor=None,
                 sizes=None, fill_empty=False, barb_increments=None,
                 rounding=True, flip_barb=False, **kw):
        """
        The constructor takes one required argument, an Axes
        instance, followed by the args and kwargs described
        by the following pyplot interface documentation:
        %(barbs_doc)s
        """
        self.sizes = sizes or dict()
        self.fill_empty = fill_empty
        self.barb_increments = barb_increments or dict()
        self.rounding = rounding
        self.flip = np.atleast_1d(flip_barb)
        transform = kw.pop('transform', ax.transData)
        self._pivot = pivot
        self._length = length
        barbcolor = barbcolor
        flagcolor = flagcolor

        # Flagcolor and barbcolor provide convenience parameters for
        # setting the facecolor and edgecolor, respectively, of the barb
        # polygon.  We also work here to make the flag the same color as the
        # rest of the barb by default

        if None in (barbcolor, flagcolor):
            kw['edgecolors'] = 'face'
            if flagcolor:
                kw['facecolors'] = flagcolor
            elif barbcolor:
                kw['facecolors'] = barbcolor
            else:
                # Set to facecolor passed in or default to black
                kw.setdefault('facecolors', 'k')
        else:
            kw['edgecolors'] = barbcolor
            kw['facecolors'] = flagcolor

        # Explicitly set a line width if we're not given one, otherwise
        # polygons are not outlined and we get no barbs
        if 'linewidth' not in kw and 'lw' not in kw:
            kw['linewidth'] = 1

        # Parse out the data arrays from the various configurations supported
        x, y, u, v, c = _parse_args(*args, caller_name='barbs()')
        self.x = x
        self.y = y
        xy = np.column_stack((x, y))

        # Make a collection
        barb_size = self._length ** 2 / 4  # Empirically determined
        super().__init__([], (barb_size,), offsets=xy, transOffset=transform,
                         **kw)
        self.set_transform(transforms.IdentityTransform())

        self.set_UVC(u, v, c)
