    def _get_agg_axis(self, axis_num: int) -> Index:
        """
        Let's be explicit about this.
        """
        if axis_num == 0:
            return self.columns
        elif axis_num == 1:
            return self.index
        else:
            raise ValueError(f"Axis must be 0 or 1 (got {repr(axis_num)})")
