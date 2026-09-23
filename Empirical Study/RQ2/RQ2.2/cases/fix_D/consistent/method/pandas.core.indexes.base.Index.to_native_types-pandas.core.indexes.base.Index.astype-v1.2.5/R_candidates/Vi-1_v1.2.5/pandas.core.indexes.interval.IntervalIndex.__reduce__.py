    def __reduce__(self):
        d = {"left": self.left, "right": self.right}
        d.update(self._get_attributes_dict())
        return _new_IntervalIndex, (type(self), d), None
