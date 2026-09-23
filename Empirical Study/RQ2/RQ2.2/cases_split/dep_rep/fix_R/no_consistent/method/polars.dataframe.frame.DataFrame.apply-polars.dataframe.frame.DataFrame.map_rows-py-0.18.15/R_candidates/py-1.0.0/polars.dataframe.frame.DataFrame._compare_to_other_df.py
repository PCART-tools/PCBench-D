    def _compare_to_other_df(
        self,
        other: DataFrame,
        op: ComparisonOperator,
    ) -> DataFrame:
        """Compare a DataFrame with another DataFrame."""
        if self.columns != other.columns:
            msg = "DataFrame columns do not match"
            raise ValueError(msg)
        if self.shape != other.shape:
            msg = "DataFrame dimensions do not match"
            raise ValueError(msg)

        suffix = "__POLARS_CMP_OTHER"
        other_renamed = other.select(F.all().name.suffix(suffix))
        combined = F.concat([self, other_renamed], how="horizontal")

        if op == "eq":
            expr = [F.col(n) == F.col(f"{n}{suffix}") for n in self.columns]
        elif op == "neq":
            expr = [F.col(n) != F.col(f"{n}{suffix}") for n in self.columns]
        elif op == "gt":
            expr = [F.col(n) > F.col(f"{n}{suffix}") for n in self.columns]
        elif op == "lt":
            expr = [F.col(n) < F.col(f"{n}{suffix}") for n in self.columns]
        elif op == "gt_eq":
            expr = [F.col(n) >= F.col(f"{n}{suffix}") for n in self.columns]
        elif op == "lt_eq":
            expr = [F.col(n) <= F.col(f"{n}{suffix}") for n in self.columns]
        else:
            msg = f"unexpected comparison operator {op!r}"
            raise ValueError(msg)

        return combined.select(expr)
