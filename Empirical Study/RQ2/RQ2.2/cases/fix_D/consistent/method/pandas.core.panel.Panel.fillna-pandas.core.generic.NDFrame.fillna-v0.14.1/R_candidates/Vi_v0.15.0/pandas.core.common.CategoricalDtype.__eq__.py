    def __eq__(self, other):
        if isinstance(other, compat.string_types):
            return other == self.name

        return isinstance(other, CategoricalDtype)
