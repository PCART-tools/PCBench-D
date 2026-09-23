    def __init__(self, env, engine, parser, **kwargs) -> None:
        super().__init__(env, engine, parser)
        for bin_op in self.binary_ops:
            bin_node = self.binary_op_nodes_map[bin_op]
            setattr(
                self,
                f"visit_{bin_node}",
                lambda node, bin_op=bin_op: partial(BinOp, bin_op, **kwargs),
            )
