    def __deepcopy__(self, memo):
        # We could deepcopy the entire transform tree, but nothing except
        # `self` is accessible publicly, so we may as well just freeze `self`.
        other = self.frozen()
        if other is not self:
            return other
        # Some classes implement frozen() as returning self, which is not
        # acceptable for deepcopying, so we need to handle them separately.
        other = copy.deepcopy(super(), memo)
        # If `c = a + b; a1 = copy(a)`, then modifications to `a1` do not
        # propagate back to `c`, i.e. we need to clear the parents of `a1`.
        other._parents = {}
        # If `c = a + b; c1 = copy(c)`, this creates a separate tree
        # (`c1 = a1 + b1`) so nothing needs to be done.
        return other
