    def _should_reindex_frame_op(self, right, op, axis: int, fill_value, level) -> bool:
        """
        Check if this is an operation between DataFrames that will need to reindex.
        """
        if op is operator.pow or op is roperator.rpow:
            # GH#32685 pow has special semantics for operating with null values
            return False

        if not isinstance(right, DataFrame):
            return False

        if fill_value is None and level is None and axis == 1:
            # TODO: any other cases we should handle here?

            # Intersection is always unique so we have to check the unique columns
            left_uniques = self.columns.unique()
            right_uniques = right.columns.unique()
            cols = left_uniques.intersection(right_uniques)
            if len(cols) and not (
                len(cols) == len(left_uniques) and len(cols) == len(right_uniques)
            ):
                # TODO: is there a shortcut available when len(cols) == 0?
                return True

        return False
