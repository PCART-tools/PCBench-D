    @property
    def operand_types(self):
        return frozenset(term.type for term in com.flatten(self))
