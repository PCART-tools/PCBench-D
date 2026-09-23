    def _wrap_union_result(self, other, result):
        name = self.name if self.name == other.name else None
        return type(self)(data=result, name=name)
