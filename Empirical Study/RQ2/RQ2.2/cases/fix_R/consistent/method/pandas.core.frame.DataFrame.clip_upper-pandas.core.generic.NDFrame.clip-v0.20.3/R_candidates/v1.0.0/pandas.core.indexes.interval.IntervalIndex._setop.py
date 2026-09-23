    def _setop(op_name: str, sort=None):
        @SetopCheck(op_name=op_name)
        def func(self, other, sort=sort):
            result = getattr(self._multiindex, op_name)(other._multiindex, sort=sort)
            result_name = get_op_result_name(self, other)

            # GH 19101: ensure empty results have correct dtype
            if result.empty:
                result = result.values.astype(self.dtype.subtype)
            else:
                result = result.values

            return type(self).from_tuples(result, closed=self.closed, name=result_name)

        return func
