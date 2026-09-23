    def update(self, left=None, bottom=None, right=None, top=None,
               wspace=None, hspace=None):
        """
        Update the dimensions of the passed parameters. *None* means unchanged.
        """
        if self._validate:
            if ((left if left is not None else self.left)
                    >= (right if right is not None else self.right)):
                raise ValueError('left cannot be >= right')
            if ((bottom if bottom is not None else self.bottom)
                    >= (top if top is not None else self.top)):
                raise ValueError('bottom cannot be >= top')
        if left is not None:
            self.left = left
        if right is not None:
            self.right = right
        if bottom is not None:
            self.bottom = bottom
        if top is not None:
            self.top = top
        if wspace is not None:
            self.wspace = wspace
        if hspace is not None:
            self.hspace = hspace
