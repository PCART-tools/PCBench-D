    def __reduce__(self):
        d = dict(left=self.left,
                 right=self.right)
        d.update(self._get_attributes_dict())
        return _new_IntervalIndex, (self.__class__, d), None
