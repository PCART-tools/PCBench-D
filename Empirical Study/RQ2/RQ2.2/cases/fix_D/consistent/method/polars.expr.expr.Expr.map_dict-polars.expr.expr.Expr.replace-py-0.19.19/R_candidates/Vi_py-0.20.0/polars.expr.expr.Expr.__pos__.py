    def __pos__(self) -> Expr:
        pos_expr = F.lit(0) + self
        if (name := self.meta.output_name(raise_if_undetermined=False)) is not None:
            pos_expr = pos_expr.alias(name)
        return pos_expr
