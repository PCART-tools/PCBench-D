    def _slice_axis_for_step(self, index: Index, result: Sized | None = None) -> Index:
        """
        Slices the index for a given result and the preset step.
        """
        return (
            index
            if result is None or len(result) == len(index)
            else index[:: self.step]
        )
