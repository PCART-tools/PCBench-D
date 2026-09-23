        def __radd__(self, other):
            if isinstance(other, list):
                return other + list(self)
            return NotImplemented
