    def _clip_with_one_bound(self, threshold, method, axis, inplace):

        inplace = validate_bool_kwarg(inplace, 'inplace')
        if axis is not None:
            axis = self._get_axis_number(axis)

        # method is self.le for upper bound and self.ge for lower bound
        if is_scalar(threshold) and is_number(threshold):
            if method.__name__ == 'le':
                return self._clip_with_scalar(None, threshold, inplace=inplace)
            return self._clip_with_scalar(threshold, None, inplace=inplace)

        subset = method(threshold, axis=axis) | isna(self)

        # GH #15390
        # In order for where method to work, the threshold must
        # be transformed to NDFrame from other array like structure.
        if (not isinstance(threshold, ABCSeries)) and is_list_like(threshold):
            if isinstance(self, ABCSeries):
                threshold = pd.Series(threshold, index=self.index)
            else:
                threshold = _align_method_FRAME(self, np.asarray(threshold),
                                                axis)
        return self.where(subset, threshold, axis=axis, inplace=inplace)
