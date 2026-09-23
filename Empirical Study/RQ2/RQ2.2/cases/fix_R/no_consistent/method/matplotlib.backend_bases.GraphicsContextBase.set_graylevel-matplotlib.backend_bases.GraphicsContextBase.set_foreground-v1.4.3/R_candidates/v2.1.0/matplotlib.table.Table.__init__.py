    def __init__(self, ax, loc=None, bbox=None, **kwargs):

        Artist.__init__(self)

        if isinstance(loc, six.string_types) and loc not in self.codes:
            warnings.warn('Unrecognized location %s. Falling back on '
                          'bottom; valid locations are\n%s\t' %
                          (loc, '\n\t'.join(self.codes)))
            loc = 'bottom'
        if isinstance(loc, six.string_types):
            loc = self.codes.get(loc, 1)
        self.set_figure(ax.figure)
        self._axes = ax
        self._loc = loc
        self._bbox = bbox

        # use axes coords
        self.set_transform(ax.transAxes)

        self._texts = []
        self._cells = {}
        self._edges = None
        self._autoRows = []
        self._autoColumns = []
        self._autoFontsize = True
        self.update(kwargs)

        self.set_clip_on(False)
