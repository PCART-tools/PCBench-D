    def min(self, skipna: bool = True, **kwargs) -> Scalar:
        nv.validate_min((), kwargs)
        result = masked_reductions.min(
            values=self.to_numpy(), mask=self.isna(), skipna=skipna
        )
        return result
