    def _align_for_op(self, right, align_asobject: bool = False):
        """align lhs and rhs Series"""
        # TODO: Different from DataFrame._align_for_op, list, tuple and ndarray
        # are not coerced here
        # because Series has inconsistencies described in GH#13637
        left = self

        if isinstance(right, Series):
            # avoid repeated alignment
            if not left.index.equals(right.index):
                if align_asobject:
                    if left.dtype not in (object, np.bool_) or right.dtype not in (
                        object,
                        np.bool_,
                    ):
                        warnings.warn(
                            "Operation between non boolean Series with different "
                            "indexes will no longer return a boolean result in "
                            "a future version. Cast both Series to object type "
                            "to maintain the prior behavior.",
                            FutureWarning,
                            stacklevel=find_stack_level(),
                        )
                    # to keep original value's dtype for bool ops
                    left = left.astype(object)
                    right = right.astype(object)

                left, right = left.align(right, copy=False)

        return left, right
