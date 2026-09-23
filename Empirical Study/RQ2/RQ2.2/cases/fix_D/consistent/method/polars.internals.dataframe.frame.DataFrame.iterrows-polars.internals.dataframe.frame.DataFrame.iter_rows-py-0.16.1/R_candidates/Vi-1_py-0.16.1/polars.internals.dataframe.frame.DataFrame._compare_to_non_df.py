    def _compare_to_non_df(
        self: DF,
        other: Any,
        op: ComparisonOperator,
    ) -> DF:
        """Compare a DataFrame with a non-DataFrame object."""
        if op == "eq":
            return self.select(pli.all() == other)
        elif op == "neq":
            return self.select(pli.all() != other)
        elif op == "gt":
            return self.select(pli.all() > other)
        elif op == "lt":
            return self.select(pli.all() < other)
        elif op == "gt_eq":
            return self.select(pli.all() >= other)
        elif op == "lt_eq":
            return self.select(pli.all() <= other)
        else:
            raise ValueError(f"got unexpected comparison operator: {op}")
