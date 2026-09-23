    @copy(str_translate)
    def translate(self, table, deletechars=None):
        result = str_translate(self.series, table, deletechars)
        return self._wrap_result(result)
