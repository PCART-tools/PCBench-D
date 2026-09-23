    def _wrap_union_result(self, other, result):
        name = self.name if self.name == other.name else None
        return self._simple_new(result, name=name, freq=None)
