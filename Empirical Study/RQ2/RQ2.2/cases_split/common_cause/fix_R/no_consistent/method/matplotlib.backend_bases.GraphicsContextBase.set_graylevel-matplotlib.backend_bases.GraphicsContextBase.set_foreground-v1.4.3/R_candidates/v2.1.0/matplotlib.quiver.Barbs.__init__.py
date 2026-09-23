    @docstring.interpd
    def __init__(self, ax, *args, **kw):
        """
        The constructor takes one required argument, an Axes
        instance, followed by the args and kwargs described
        by the following pylab interface documentation:
        %(barbs_doc)s
        """
        self._pivot = kw.pop('pivot', 'tip')
        self._length = kw.pop('length', 7)
        barbcolor = kw.pop('barbcolor', None)
        flagcolor = kw.pop('flagcolor', None)
        self.sizes = kw.pop('sizes', dict())
        self.fill_empty = kw.pop('fill_empty', False)
        self.barb_increments = kw.pop('barb_increments', dict())
        self.rounding = kw.pop('rounding', True)
        self.flip = kw.pop('flip_barb', False)
        transform = kw.pop('transform', ax.transData)

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
        x, y, u, v, c = _parse_args(*args)
        self.x = x
        self.y = y
        xy = np.hstack((x[:, np.newaxis], y[:, np.newaxis]))

        # Make a collection
        barb_size = self._length ** 2 / 4  # Empirically determined
        mcollections.PolyCollection.__init__(self, [], (barb_size,),
                                             offsets=xy,
                                             transOffset=transform, **kw)
        self.set_transform(transforms.IdentityTransform())

        self.set_UVC(u, v, c)
