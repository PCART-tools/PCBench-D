    def __neg__(self) -> Expr:
        neg_expr = F.lit(0) - self
        if (name := self.meta.output_name(raise_if_undetermined=False)) is not None:
            neg_expr = neg_expr.alias(name)
        return neg_expr
