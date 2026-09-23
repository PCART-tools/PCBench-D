    def __init__(self, op: Literal["+", "-", "~", "not"], operand) -> None:
        super().__init__(op, (operand,))
        self.operand = operand

        try:
            self.func = _unary_ops_dict[op]
        except KeyError as err:
            raise ValueError(
                f"Invalid unary operator {repr(op)}, "
                f"valid operators are {UNARY_OPS_SYMS}"
            ) from err
