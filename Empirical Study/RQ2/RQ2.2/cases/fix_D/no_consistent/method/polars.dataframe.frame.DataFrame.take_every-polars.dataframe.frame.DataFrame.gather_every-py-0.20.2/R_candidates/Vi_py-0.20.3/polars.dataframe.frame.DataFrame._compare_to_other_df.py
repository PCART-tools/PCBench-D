    def _compare_to_other_df(
        self,
        other: DataFrame,
        op: ComparisonOperator,
    ) -> DataFrame:
        """Compare a DataFrame with another DataFrame."""
        if self.columns != other.columns:
            raise ValueError("DataFrame columns do not match")
        if self.shape != other.shape:
            raise ValueError("DataFrame dimensions do not match")

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
            raise ValueError(f"unexpected comparison operator {op!r}")

        return combined.select(expr)
