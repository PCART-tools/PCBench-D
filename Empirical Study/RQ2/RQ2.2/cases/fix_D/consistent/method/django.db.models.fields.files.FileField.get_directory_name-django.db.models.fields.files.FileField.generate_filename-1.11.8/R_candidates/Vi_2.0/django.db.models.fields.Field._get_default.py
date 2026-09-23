    @cached_property
    def _get_default(self):
        if self.has_default():
            if callable(self.default):
                return self.default
            return lambda: self.default

        if not self.empty_strings_allowed or self.null and not connection.features.interprets_empty_strings_as_nulls:
            return return_None
        return str  # return empty string
