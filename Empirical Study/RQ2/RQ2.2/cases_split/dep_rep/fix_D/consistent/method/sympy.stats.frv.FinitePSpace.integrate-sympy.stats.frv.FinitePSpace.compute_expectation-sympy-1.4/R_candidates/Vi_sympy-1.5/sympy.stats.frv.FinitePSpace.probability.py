    def probability(self, condition):
        cond_symbols = frozenset(rs.symbol for rs in random_symbols(condition))
        cond = rv_subs(condition)
        if not cond_symbols.issubset(self.symbols):
            raise ValueError("Cannot compare foreign random symbols, %s"
                             %(str(cond_symbols - self.symbols)))
        if isinstance(condition, Relational) and \
            (not cond.free_symbols.issubset(self.domain.free_symbols)):
            rv = condition.lhs if isinstance(condition.rhs, Symbol) else condition.rhs
            return sum(Piecewise(
                       (self.prob_of(elem), condition.subs(rv, list(elem)[0][1])),
                       (S.Zero, True)) for elem in self.domain)
        return sympify(sum(self.prob_of(elem) for elem in self.where(condition)))
