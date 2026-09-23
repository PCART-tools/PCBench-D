    def _convert_can_do_setop(self, other):
        if not isinstance(other, Index):
            other = Index(other, name=self.name)
            result_name = self.name
        else:
            result_name = self.name if self.name == other.name else None
        return other, result_name
