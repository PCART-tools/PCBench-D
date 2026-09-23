    @copy(str_get_dummies)
    def get_dummies(self, sep='|'):
        result = str_get_dummies(self.series, sep)
        return self._wrap_result(result)
