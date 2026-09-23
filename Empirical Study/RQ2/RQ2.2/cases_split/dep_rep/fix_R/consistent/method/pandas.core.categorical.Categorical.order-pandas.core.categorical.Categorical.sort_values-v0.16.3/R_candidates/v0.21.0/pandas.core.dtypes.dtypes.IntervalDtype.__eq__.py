    def __eq__(self, other):
        if isinstance(other, compat.string_types):
            return other == self.name or other == self.name.title()

        return (isinstance(other, IntervalDtype) and
                self.subtype == other.subtype)
