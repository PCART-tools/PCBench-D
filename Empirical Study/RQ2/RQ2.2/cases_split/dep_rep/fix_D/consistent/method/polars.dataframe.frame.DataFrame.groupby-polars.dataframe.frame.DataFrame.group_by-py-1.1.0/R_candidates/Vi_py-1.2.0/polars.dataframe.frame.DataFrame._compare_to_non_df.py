    def _compare_to_non_df(
        self,
        other: Any,
        op: ComparisonOperator,
    ) -> DataFrame:
        """Compare a DataFrame with a non-DataFrame object."""
        warn_null_comparison(other)
        if op == "eq":
            return self.select(F.all() == other)
        elif op == "neq":
            return self.select(F.all() != other)
        elif op == "gt":
            return self.select(F.all() > other)
        elif op == "lt":
            return self.select(F.all() < other)
        elif op == "gt_eq":
            return self.select(F.all() >= other)
        elif op == "lt_eq":
            return self.select(F.all() <= other)
        else:
            msg = f"unexpected comparison operator {op!r}"
            raise ValueError(msg)
