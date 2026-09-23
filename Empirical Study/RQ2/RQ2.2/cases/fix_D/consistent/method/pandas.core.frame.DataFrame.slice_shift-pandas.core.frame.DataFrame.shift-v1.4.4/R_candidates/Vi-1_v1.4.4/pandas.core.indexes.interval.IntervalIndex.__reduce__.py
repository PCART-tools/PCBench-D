    def __reduce__(self):
        d = {
            "left": self.left,
            "right": self.right,
            "closed": self.closed,
            "name": self.name,
        }
        return _new_IntervalIndex, (type(self), d), None
