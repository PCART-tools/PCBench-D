    def copy(self):
        """ Copy constructor. """
        return Categorical(values=self._codes.copy(),categories=self.categories,
                           name=self.name, ordered=self.ordered, fastpath=True)
