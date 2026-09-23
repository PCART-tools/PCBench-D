    @copy(str_repeat)
    def repeat(self, repeats):
        result = str_repeat(self._parent, repeats)
        return self._wrap_result(result)
