    @final
    def _clip_with_scalar(self, lower, upper, inplace: bool_t = False):
        if (lower is not None and np.any(isna(lower))) or (
            upper is not None and np.any(isna(upper))
        ):
            raise ValueError("Cannot use an NA value as a clip threshold")

        result = self
        mask = isna(self._values)

        with np.errstate(all="ignore"):
            if upper is not None:
                subset = self <= upper
                result = result.where(subset, upper, axis=None, inplace=False)
            if lower is not None:
                subset = self >= lower
                result = result.where(subset, lower, axis=None, inplace=False)

        if np.any(mask):
            result[mask] = np.nan

        if inplace:
            return self._update_inplace(result)
        else:
            return result
