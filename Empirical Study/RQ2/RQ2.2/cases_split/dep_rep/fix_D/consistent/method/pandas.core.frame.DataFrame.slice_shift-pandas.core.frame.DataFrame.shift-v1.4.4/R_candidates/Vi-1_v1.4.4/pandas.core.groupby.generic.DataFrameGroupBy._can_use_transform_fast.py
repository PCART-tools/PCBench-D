    def _can_use_transform_fast(self, result) -> bool:
        return isinstance(result, DataFrame) and result.columns.equals(
            self._obj_with_exclusions.columns
        )
