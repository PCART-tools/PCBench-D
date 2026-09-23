    def prob_of(self, elem):
        elem = sympify(elem)
        return self._density.get(elem, 0)
