    @copy(str_center)
    def center(self, width):
        result = str_center(self.series, width)
        return self._wrap_result(result)
