    def __init__(self, parent, orientation,
                  location, functions, **kwargs):
        """
        See `.secondary_xaxis` and `.secondary_yaxis` for the doc string.
        While there is no need for this to be private, it should really be
        called by those higher level functions.
        """

        self._functions = functions
        self._parent = parent
        self._orientation = orientation
        self._ticks_set = False

        if self._orientation == 'x':
            super().__init__(self._parent.figure, [0, 1., 1, 0.0001], **kwargs)
            self._axis = self.xaxis
            self._locstrings = ['top', 'bottom']
            self._otherstrings = ['left', 'right']
        elif self._orientation == 'y':
            super().__init__(self._parent.figure, [0, 1., 0.0001, 1], **kwargs)
            self._axis = self.yaxis
            self._locstrings = ['right', 'left']
            self._otherstrings = ['top', 'bottom']
        # this gets positioned w/o constrained_layout so exclude:
        self._layoutbox = None
        self._poslayoutbox = None

        self.set_location(location)
        self.set_functions(functions)

        # styling:
        if self._orientation == 'x':
            otheraxis = self.yaxis
        else:
            otheraxis = self.xaxis

        otheraxis.set_major_locator(mticker.NullLocator())
        otheraxis.set_ticks_position('none')

        for st in self._otherstrings:
            self.spines[st].set_visible(False)
        for st in self._locstrings:
            self.spines[st].set_visible(True)

        if self._pos < 0.5:
            # flip the location strings...
            self._locstrings = self._locstrings[::-1]
        self.set_alignment(self._locstrings[0])
