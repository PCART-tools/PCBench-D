    def _concat(self, to_concat, name):

        typs = _concat.get_dtype_kinds(to_concat)

        if len(typs) == 1:
            return self._concat_same_dtype(to_concat, name=name)
        return Index._concat_same_dtype(self, to_concat, name=name)
