    def _setop(op_name):
        def func(self, other, sort=True):
            other = self._as_like_interval_index(other)

            # GH 19016: ensure set op will not return a prohibited dtype
            subtypes = [self.dtype.subtype, other.dtype.subtype]
            common_subtype = find_common_type(subtypes)
            if is_object_dtype(common_subtype):
                msg = ('can only do {op} between two IntervalIndex '
                       'objects that have compatible dtypes')
                raise TypeError(msg.format(op=op_name))

            result = getattr(self._multiindex, op_name)(other._multiindex,
                                                        sort=sort)
            result_name = get_op_result_name(self, other)

            # GH 19101: ensure empty results have correct dtype
            if result.empty:
                result = result.values.astype(self.dtype.subtype)
            else:
                result = result.values

            return type(self).from_tuples(result, closed=self.closed,
                                          name=result_name)
        return func
