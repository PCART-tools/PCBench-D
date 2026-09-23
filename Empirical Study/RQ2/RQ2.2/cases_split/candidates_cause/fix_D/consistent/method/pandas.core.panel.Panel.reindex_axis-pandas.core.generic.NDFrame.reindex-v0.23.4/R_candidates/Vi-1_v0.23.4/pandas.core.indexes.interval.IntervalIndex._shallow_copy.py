    @Appender(_index_shared_docs['_shallow_copy'])
    def _shallow_copy(self, left=None, right=None, **kwargs):
        if left is None:

            # no values passed
            left, right = self.left, self.right

        elif right is None:

            # only single value passed, could be an IntervalIndex
            # or array of Intervals
            if not isinstance(left, IntervalIndex):
                left = self._constructor(left)

            left, right = left.left, left.right
        else:

            # both left and right are values
            pass

        attributes = self._get_attributes_dict()
        attributes.update(kwargs)
        attributes['verify_integrity'] = False
        return self._simple_new(left, right, **attributes)
