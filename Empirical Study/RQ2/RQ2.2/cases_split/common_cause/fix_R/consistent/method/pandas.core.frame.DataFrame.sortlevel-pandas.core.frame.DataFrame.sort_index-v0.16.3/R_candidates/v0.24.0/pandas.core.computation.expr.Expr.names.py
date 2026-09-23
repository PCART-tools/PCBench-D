    @property
    def names(self):
        """Get the names in an expression"""
        if is_term(self.terms):
            return frozenset([self.terms.name])
        return frozenset(term.name for term in com.flatten(self.terms))
