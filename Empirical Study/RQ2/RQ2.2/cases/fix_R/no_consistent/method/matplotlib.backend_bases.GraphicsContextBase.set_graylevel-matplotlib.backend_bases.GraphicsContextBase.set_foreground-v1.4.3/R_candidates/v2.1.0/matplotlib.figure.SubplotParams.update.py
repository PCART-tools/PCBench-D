    def update(self, left=None, bottom=None, right=None, top=None,
               wspace=None, hspace=None):
        """
        Update the current values.  If any kwarg is None, default to
        the current value, if set, otherwise to rc

        """

        thisleft = getattr(self, 'left', None)
        thisright = getattr(self, 'right', None)
        thistop = getattr(self, 'top', None)
        thisbottom = getattr(self, 'bottom', None)
        thiswspace = getattr(self, 'wspace', None)
        thishspace = getattr(self, 'hspace', None)

        self._update_this('left', left)
        self._update_this('right', right)
        self._update_this('bottom', bottom)
        self._update_this('top', top)
        self._update_this('wspace', wspace)
        self._update_this('hspace', hspace)

        def reset():
            self.left = thisleft
            self.right = thisright
            self.top = thistop
            self.bottom = thisbottom
            self.wspace = thiswspace
            self.hspace = thishspace

        if self.validate:
            if self.left >= self.right:
                reset()
                raise ValueError('left cannot be >= right')

            if self.bottom >= self.top:
                reset()
                raise ValueError('bottom cannot be >= top')
