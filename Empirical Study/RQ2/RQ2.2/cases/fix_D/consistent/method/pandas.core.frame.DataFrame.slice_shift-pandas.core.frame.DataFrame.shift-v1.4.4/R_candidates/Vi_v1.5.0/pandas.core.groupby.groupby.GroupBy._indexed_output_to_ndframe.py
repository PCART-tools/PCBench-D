    def _indexed_output_to_ndframe(
        self, result: Mapping[base.OutputKey, ArrayLike]
    ) -> Series | DataFrame:
        raise AbstractMethodError(self)
