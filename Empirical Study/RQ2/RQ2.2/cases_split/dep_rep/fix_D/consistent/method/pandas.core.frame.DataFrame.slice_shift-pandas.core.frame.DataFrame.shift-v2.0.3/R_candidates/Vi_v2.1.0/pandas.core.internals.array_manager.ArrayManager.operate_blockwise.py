    def operate_blockwise(self, other: ArrayManager, array_op) -> ArrayManager:
        """
        Apply array_op blockwise with another (aligned) BlockManager.
        """
        # TODO what if `other` is BlockManager ?
        left_arrays = self.arrays
        right_arrays = other.arrays
        result_arrays = [
            array_op(left, right) for left, right in zip(left_arrays, right_arrays)
        ]
        return type(self)(result_arrays, self._axes)
