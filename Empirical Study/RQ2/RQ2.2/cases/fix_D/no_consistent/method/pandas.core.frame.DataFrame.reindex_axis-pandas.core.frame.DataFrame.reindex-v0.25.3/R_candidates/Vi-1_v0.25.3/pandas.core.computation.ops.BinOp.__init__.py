    def __init__(self, op, lhs, rhs, **kwargs):
        super().__init__(op, (lhs, rhs))
        self.lhs = lhs
        self.rhs = rhs

        self._disallow_scalar_only_bool_ops()

        self.convert_values()

        try:
            self.func = _binary_ops_dict[op]
        except KeyError:
            # has to be made a list for python3
            keys = list(_binary_ops_dict.keys())
            raise ValueError(
                "Invalid binary operator {0!r}, valid"
                " operators are {1}".format(op, keys)
            )
