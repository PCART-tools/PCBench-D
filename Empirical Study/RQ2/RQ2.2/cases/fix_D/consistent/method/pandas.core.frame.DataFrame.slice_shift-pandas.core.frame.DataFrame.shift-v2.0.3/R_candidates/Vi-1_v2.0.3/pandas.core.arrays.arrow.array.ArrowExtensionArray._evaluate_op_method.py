    def _evaluate_op_method(self, other, op, arrow_funcs):
        from pandas.core.arrays.masked import BaseMaskedArray

        pa_type = self._data.type
        if (pa.types.is_string(pa_type) or pa.types.is_binary(pa_type)) and op in [
            operator.add,
            roperator.radd,
        ]:
            length = self._data.length()

            seps: list[str] | list[bytes]
            if pa.types.is_string(pa_type):
                seps = [""] * length
            else:
                seps = [b""] * length

            if is_scalar(other):
                other = [other] * length
            elif isinstance(other, type(self)):
                other = other._data
            if op is operator.add:
                result = pc.binary_join_element_wise(self._data, other, seps)
            else:
                result = pc.binary_join_element_wise(other, self._data, seps)
            return type(self)(result)

        pc_func = arrow_funcs[op.__name__]
        if pc_func is NotImplemented:
            raise NotImplementedError(f"{op.__name__} not implemented.")
        if isinstance(other, ArrowExtensionArray):
            result = pc_func(self._data, other._data)
        elif isinstance(other, (np.ndarray, list)):
            result = pc_func(self._data, pa.array(other, from_pandas=True))
        elif isinstance(other, BaseMaskedArray):
            # GH 52625
            result = pc_func(self._data, other.__arrow_array__())
        elif is_scalar(other):
            if isna(other) and op.__name__ in ARROW_LOGICAL_FUNCS:
                # pyarrow kleene ops require null to be typed
                pa_scalar = pa.scalar(None, type=self._data.type)
            else:
                pa_scalar = pa.scalar(other)
            result = pc_func(self._data, pa_scalar)
        else:
            raise NotImplementedError(
                f"{op.__name__} not implemented for {type(other)}"
            )
        return type(self)(result)
