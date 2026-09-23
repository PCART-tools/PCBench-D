    def _resolve_output(self, out: DataFrame, obj: DataFrame) -> DataFrame:
        """Validate and finalize result."""
        if out.shape[1] == 0 and obj.shape[1] > 0:
            raise DataError("No numeric types to aggregate")
        elif out.shape[1] == 0:
            return obj.astype("float64")

        self._insert_on_column(out, obj)
        return out
