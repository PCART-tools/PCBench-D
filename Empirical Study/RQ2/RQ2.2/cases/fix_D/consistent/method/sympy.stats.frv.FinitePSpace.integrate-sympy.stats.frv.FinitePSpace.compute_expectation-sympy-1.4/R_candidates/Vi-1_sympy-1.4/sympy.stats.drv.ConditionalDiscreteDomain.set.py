    @property
    def set(self):
        rv = self.symbols
        if len(self.symbols) > 1:
            raise NotImplementedError(filldedent('''
                Multivariate condtional domains are not yet implemented.'''))
        rv = list(rv)[0]
        return reduce_rational_inequalities_wrap(self.condition,
            rv).intersect(self.fulldomain.set)
