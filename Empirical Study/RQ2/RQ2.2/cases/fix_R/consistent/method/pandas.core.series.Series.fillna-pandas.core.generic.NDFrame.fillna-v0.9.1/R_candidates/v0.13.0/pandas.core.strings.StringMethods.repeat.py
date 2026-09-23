    @copy(str_repeat)
    def repeat(self, repeats):
        result = str_repeat(self.series, repeats)
        return self._wrap_result(result)
