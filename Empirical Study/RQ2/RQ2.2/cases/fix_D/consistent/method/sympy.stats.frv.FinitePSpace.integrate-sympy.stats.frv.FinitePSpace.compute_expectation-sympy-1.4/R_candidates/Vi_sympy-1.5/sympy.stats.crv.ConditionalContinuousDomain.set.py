    @property
    def set(self):
        if len(self.symbols) == 1:
            return (self.fulldomain.set & reduce_rational_inequalities_wrap(
                self.condition, tuple(self.symbols)[0]))
        else:
            raise NotImplementedError(
                "Set of Conditional Domain not Implemented")
