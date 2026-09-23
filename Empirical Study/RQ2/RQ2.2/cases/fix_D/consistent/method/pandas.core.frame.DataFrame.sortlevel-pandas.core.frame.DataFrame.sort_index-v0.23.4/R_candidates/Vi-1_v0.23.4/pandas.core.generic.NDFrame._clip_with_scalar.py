    def _clip_with_scalar(self, lower, upper, inplace=False):
        if ((lower is not None and np.any(isna(lower))) or
                (upper is not None and np.any(isna(upper)))):
            raise ValueError("Cannot use an NA value as a clip threshold")

        result = self.values
        mask = isna(result)

        with np.errstate(all='ignore'):
            if upper is not None:
                result = np.where(result >= upper, upper, result)
            if lower is not None:
                result = np.where(result <= lower, lower, result)
        if np.any(mask):
            result[mask] = np.nan

        axes_dict = self._construct_axes_dict()
        result = self._constructor(result, **axes_dict).__finalize__(self)

        if inplace:
            self._update_inplace(result)
        else:
            return result
