    def __add__(self, other):
        if isinstance(other, _Base):
            return Add(self, other)
        else:
            return Add(self, Fixed(other))
