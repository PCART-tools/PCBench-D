    def _unary_method(self, op):
        result = op(self._values)
        return Index(result, name=self.name)
