    def _evaluate_op_method(self, other, op, arrow_funcs):
        pc_func = arrow_funcs[op.__name__]
        if pc_func is NotImplemented:
            raise NotImplementedError(f"{op.__name__} not implemented.")
        if isinstance(other, ArrowExtensionArray):
            result = pc_func(self._data, other._data)
        elif isinstance(other, (np.ndarray, list)):
            result = pc_func(self._data, pa.array(other, from_pandas=True))
        elif is_scalar(other):
            result = pc_func(self._data, pa.scalar(other))
        else:
            raise NotImplementedError(
                f"{op.__name__} not implemented for {type(other)}"
            )
        return type(self)(result)
