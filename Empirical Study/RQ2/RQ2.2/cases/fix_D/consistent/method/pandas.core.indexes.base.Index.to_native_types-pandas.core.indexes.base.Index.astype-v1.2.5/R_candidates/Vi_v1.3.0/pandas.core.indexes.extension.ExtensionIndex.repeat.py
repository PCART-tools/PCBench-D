    def repeat(self, repeats, axis=None):
        nv.validate_repeat((), {"axis": axis})
        result = self._data.repeat(repeats, axis=axis)
        return type(self)._simple_new(result, name=self.name)
