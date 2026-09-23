    @property
    def return_type(self) -> np.dtype:
        operand = self.operand
        if operand.return_type == np.dtype("bool"):
            return np.dtype("bool")
        if isinstance(operand, Op) and (
            operand.op in _cmp_ops_dict or operand.op in _bool_ops_dict
        ):
            return np.dtype("bool")
        return np.dtype("int")
