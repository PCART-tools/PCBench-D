    def __init__(self, op, operand):
        super().__init__(op, (operand,))
        self.operand = operand

        try:
            self.func = _unary_ops_dict[op]
        except KeyError:
            raise ValueError(
                "Invalid unary operator {0!r}, valid operators "
                "are {1}".format(op, _unary_ops_syms)
            )
