    def _evaluate_op_method(self, other, op, arrow_funcs):
        pa_type = self._pa_array.type
        other = self._box_pa(other)

        if (pa.types.is_string(pa_type) or pa.types.is_binary(pa_type)) and op in [
            operator.add,
            roperator.radd,
        ]:
            sep = pa.scalar("", type=pa_type)
            if op is operator.add:
                result = pc.binary_join_element_wise(self._pa_array, other, sep)
            else:
                result = pc.binary_join_element_wise(other, self._pa_array, sep)
            return type(self)(result)

        if (
            isinstance(other, pa.Scalar)
            and pc.is_null(other).as_py()
            and op.__name__ in ARROW_LOGICAL_FUNCS
        ):
            # pyarrow kleene ops require null to be typed
            other = other.cast(pa_type)

        pc_func = arrow_funcs[op.__name__]
        if pc_func is NotImplemented:
            raise NotImplementedError(f"{op.__name__} not implemented.")

        result = pc_func(self._pa_array, other)
        return type(self)(result)
