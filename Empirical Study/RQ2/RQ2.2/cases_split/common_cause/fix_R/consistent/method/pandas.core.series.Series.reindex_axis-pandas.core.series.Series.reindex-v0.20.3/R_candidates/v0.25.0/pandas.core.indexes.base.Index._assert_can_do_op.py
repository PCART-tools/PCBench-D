    def _assert_can_do_op(self, value):
        """
        Check value is valid for scalar op.
        """
        if not is_scalar(value):
            msg = "'value' must be a scalar, passed: {0}"
            raise TypeError(msg.format(type(value).__name__))
