    @cached_property
    def supports_stddev(self):
        """Confirm support for STDDEV and related stats functions."""
        try:
            self.connection.ops.check_expression_support(StdDev(1))
            return True
        except NotImplementedError:
            return False
