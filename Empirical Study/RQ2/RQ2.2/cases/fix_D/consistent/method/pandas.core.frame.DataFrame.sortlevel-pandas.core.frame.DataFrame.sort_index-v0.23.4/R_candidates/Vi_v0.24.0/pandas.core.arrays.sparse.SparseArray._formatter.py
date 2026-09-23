    def _formatter(self, boxed=False):
        # Defer to the formatter from the GenericArrayFormatter calling us.
        # This will infer the correct formatter from the dtype of the values.
        return None
