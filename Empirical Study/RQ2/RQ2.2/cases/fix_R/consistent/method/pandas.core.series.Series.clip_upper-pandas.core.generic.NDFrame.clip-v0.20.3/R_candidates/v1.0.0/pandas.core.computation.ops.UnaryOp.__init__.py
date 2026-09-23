    def __init__(self, op: str, operand):
        super().__init__(op, (operand,))
        self.operand = operand

        try:
            self.func = _unary_ops_dict[op]
        except KeyError:
            raise ValueError(
                f"Invalid unary operator {repr(op)}, "
                f"valid operators are {_unary_ops_syms}"
            )
