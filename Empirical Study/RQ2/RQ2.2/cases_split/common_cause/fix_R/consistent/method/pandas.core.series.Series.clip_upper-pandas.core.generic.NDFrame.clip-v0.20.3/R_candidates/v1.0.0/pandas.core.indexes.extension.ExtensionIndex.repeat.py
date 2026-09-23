    def repeat(self, repeats, axis=None):
        nv.validate_repeat(tuple(), dict(axis=axis))
        result = self._data.repeat(repeats, axis=axis)
        return self._shallow_copy(result)
