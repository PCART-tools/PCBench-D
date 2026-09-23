    @final
    def _clip_with_scalar(self, lower, upper, inplace: bool_t = False):
        if (lower is not None and np.any(isna(lower))) or (
            upper is not None and np.any(isna(upper))
        ):
            raise ValueError("Cannot use an NA value as a clip threshold")

        result = self
        mask = self.isna()

        if lower is not None:
            cond = mask | (self >= lower)
            result = result.where(
                cond, lower, inplace=inplace
            )  # type: ignore[assignment]
        if upper is not None:
            cond = mask | (self <= upper)
            result = self if inplace else result
            result = result.where(
                cond, upper, inplace=inplace
            )  # type: ignore[assignment]

        return result
