    def _setop(op_name: str, sort=None):
        def func(self, other, sort=sort):
            # At this point we are assured
            #  isinstance(other, IntervalIndex)
            #  other.closed == self.closed

            result = getattr(self._multiindex, op_name)(other._multiindex, sort=sort)
            result_name = get_op_result_name(self, other)

            # GH 19101: ensure empty results have correct dtype
            if result.empty:
                result = result._values.astype(self.dtype.subtype)
            else:
                result = result._values

            return type(self).from_tuples(result, closed=self.closed, name=result_name)

        func.__name__ = op_name
        return setop_check(func)
