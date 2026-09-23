    def _indexed_output_to_ndframe(
        self, output: Mapping[base.OutputKey, ArrayLike]
    ) -> Series:
        """
        Wrap the dict result of a GroupBy aggregation into a Series.
        """
        assert len(output) == 1
        values = next(iter(output.values()))
        result = self.obj._constructor(values)
        result.name = self.obj.name
        return result
