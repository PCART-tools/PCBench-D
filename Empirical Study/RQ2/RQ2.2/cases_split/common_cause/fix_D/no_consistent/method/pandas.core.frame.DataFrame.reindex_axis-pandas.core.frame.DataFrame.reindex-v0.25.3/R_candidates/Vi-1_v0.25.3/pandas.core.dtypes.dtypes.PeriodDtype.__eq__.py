    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.name or other == self.name.title()

        return isinstance(other, PeriodDtype) and self.freq == other.freq
