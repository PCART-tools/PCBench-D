    @copy(str_get_dummies)
    def get_dummies(self, sep='|'):
        # we need to cast to Series of strings as only that has all
        # methods available for making the dummies...
        data = self._orig.astype(str) if self._is_categorical else self._parent
        result, name = str_get_dummies(data, sep)
        return self._wrap_result(result, use_codes=(not self._is_categorical),
                                 name=name, expand=True)
