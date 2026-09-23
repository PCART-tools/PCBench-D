    @classmethod
    def _create_comparison_method(cls, op):
        op_name = op.__name__
        if op_name in {"and_", "or_"}:
            op_name = op_name[:-1]

        @unpack_zerodim_and_defer(op_name)
        def cmp_method(self, other):

            if not is_scalar(other) and not isinstance(other, type(self)):
                # convert list-like to ndarray
                other = np.asarray(other)

            if isinstance(other, np.ndarray):
                # TODO: make this more flexible than just ndarray...
                if len(self) != len(other):
                    raise AssertionError(
                        f"length mismatch: {len(self)} vs. {len(other)}"
                    )
                other = SparseArray(other, fill_value=self.fill_value)

            if isinstance(other, SparseArray):
                return _sparse_array_op(self, other, op, op_name)
            else:
                with np.errstate(all="ignore"):
                    fill_value = op(self.fill_value, other)
                    result = op(self.sp_values, other)

                return type(self)(
                    result,
                    sparse_index=self.sp_index,
                    fill_value=fill_value,
                    dtype=np.bool_,
                )

        name = f"__{op.__name__}__"
        return compat.set_function_name(cmp_method, name, cls)
