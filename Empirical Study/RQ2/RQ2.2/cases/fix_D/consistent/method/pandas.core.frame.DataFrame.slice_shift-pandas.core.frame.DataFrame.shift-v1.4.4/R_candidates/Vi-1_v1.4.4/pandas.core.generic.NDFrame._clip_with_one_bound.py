    @final
    def _clip_with_one_bound(self, threshold, method, axis, inplace):

        if axis is not None:
            axis = self._get_axis_number(axis)

        # method is self.le for upper bound and self.ge for lower bound
        if is_scalar(threshold) and is_number(threshold):
            if method.__name__ == "le":
                return self._clip_with_scalar(None, threshold, inplace=inplace)
            return self._clip_with_scalar(threshold, None, inplace=inplace)

        # GH #15390
        # In order for where method to work, the threshold must
        # be transformed to NDFrame from other array like structure.
        if (not isinstance(threshold, ABCSeries)) and is_list_like(threshold):
            if isinstance(self, ABCSeries):
                threshold = self._constructor(threshold, index=self.index)
            else:
                threshold = align_method_FRAME(self, threshold, axis, flex=None)[1]

        # GH 40420
        # Treat missing thresholds as no bounds, not clipping the values
        if is_list_like(threshold):
            fill_value = np.inf if method.__name__ == "le" else -np.inf
            threshold_inf = threshold.fillna(fill_value)
        else:
            threshold_inf = threshold

        subset = method(threshold_inf, axis=axis) | isna(self)

        # GH 40420
        return self.where(subset, threshold, axis=axis, inplace=inplace)
