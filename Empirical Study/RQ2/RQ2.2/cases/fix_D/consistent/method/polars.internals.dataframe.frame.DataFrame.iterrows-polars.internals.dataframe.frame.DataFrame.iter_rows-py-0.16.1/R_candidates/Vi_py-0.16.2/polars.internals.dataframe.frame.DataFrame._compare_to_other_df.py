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
        other_renamed = other.select(pli.all().suffix(suffix))
        combined = pli.concat([self, other_renamed], how="horizontal")

        if op == "eq":
            expr = [pli.col(n) == pli.col(f"{n}{suffix}") for n in self.columns]
        elif op == "neq":
            expr = [pli.col(n) != pli.col(f"{n}{suffix}") for n in self.columns]
        elif op == "gt":
            expr = [pli.col(n) > pli.col(f"{n}{suffix}") for n in self.columns]
        elif op == "lt":
            expr = [pli.col(n) < pli.col(f"{n}{suffix}") for n in self.columns]
        elif op == "gt_eq":
            expr = [pli.col(n) >= pli.col(f"{n}{suffix}") for n in self.columns]
        elif op == "lt_eq":
            expr = [pli.col(n) <= pli.col(f"{n}{suffix}") for n in self.columns]
        else:
            raise ValueError(f"got unexpected comparison operator: {op}")

        return combined.select(expr)
