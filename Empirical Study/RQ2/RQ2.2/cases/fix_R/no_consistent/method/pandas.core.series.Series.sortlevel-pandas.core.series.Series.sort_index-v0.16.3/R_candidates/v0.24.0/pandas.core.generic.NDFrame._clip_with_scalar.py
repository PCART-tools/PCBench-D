    def _clip_with_scalar(self, lower, upper, inplace=False):
        if ((lower is not None and np.any(isna(lower))) or
                (upper is not None and np.any(isna(upper)))):
            raise ValueError("Cannot use an NA value as a clip threshold")

        result = self
        mask = isna(self.values)

        with np.errstate(all='ignore'):
            if upper is not None:
                subset = self.to_numpy() <= upper
                result = result.where(subset, upper, axis=None, inplace=False)
            if lower is not None:
                subset = self.to_numpy() >= lower
                result = result.where(subset, lower, axis=None, inplace=False)

        if np.any(mask):
            result[mask] = np.nan

        if inplace:
            self._update_inplace(result)
        else:
            return result
