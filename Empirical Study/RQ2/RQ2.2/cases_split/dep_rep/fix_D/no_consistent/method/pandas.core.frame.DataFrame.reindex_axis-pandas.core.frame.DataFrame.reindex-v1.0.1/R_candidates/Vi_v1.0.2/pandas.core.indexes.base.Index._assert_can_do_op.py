    def _assert_can_do_op(self, value):
        """
        Check value is valid for scalar op.
        """
        if not is_scalar(value):
            raise TypeError(f"'value' must be a scalar, passed: {type(value).__name__}")
