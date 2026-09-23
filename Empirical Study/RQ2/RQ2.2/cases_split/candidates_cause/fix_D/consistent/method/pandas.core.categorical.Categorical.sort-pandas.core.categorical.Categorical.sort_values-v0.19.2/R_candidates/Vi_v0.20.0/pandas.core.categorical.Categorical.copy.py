    def copy(self):
        """ Copy constructor. """
        return self._constructor(values=self._codes.copy(),
                                 categories=self.categories,
                                 ordered=self.ordered,
                                 fastpath=True)
