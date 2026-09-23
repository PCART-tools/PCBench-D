        def __radd__(self, other):
            if isinstance(other, list):
                return other + list(self)
            if isinstance(other, tuple):
                return other + tuple(self)
            return NotImplemented
