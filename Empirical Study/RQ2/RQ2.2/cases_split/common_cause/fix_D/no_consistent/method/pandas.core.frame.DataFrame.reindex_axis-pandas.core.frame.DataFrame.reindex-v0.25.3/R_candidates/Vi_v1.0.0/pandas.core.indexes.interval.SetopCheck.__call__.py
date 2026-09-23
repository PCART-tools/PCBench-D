    def __call__(self, setop):
        def func(intvidx_self, other, sort=False):
            intvidx_self._assert_can_do_setop(other)
            other = ensure_index(other)

            if not isinstance(other, IntervalIndex):
                result = getattr(intvidx_self.astype(object), self.op_name)(other)
                if self.op_name in ("difference",):
                    result = result.astype(intvidx_self.dtype)
                return result
            elif intvidx_self.closed != other.closed:
                raise ValueError(
                    "can only do set operations between two IntervalIndex "
                    "objects that are closed on the same side"
                )

            # GH 19016: ensure set op will not return a prohibited dtype
            subtypes = [intvidx_self.dtype.subtype, other.dtype.subtype]
            common_subtype = find_common_type(subtypes)
            if is_object_dtype(common_subtype):
                raise TypeError(
                    f"can only do {self.op_name} between two IntervalIndex "
                    "objects that have compatible dtypes"
                )

            return setop(intvidx_self, other, sort)

        return func
