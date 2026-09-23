    def _format_data(self, name=None):
        """
        Return the formatted data as a unicode string.
        """

        # do we want to justify (only do so for non-objects)
        is_justify = not (
            self.inferred_type in ("string", "unicode")
            or (
                self.inferred_type == "categorical" and is_object_dtype(self.categories)
            )
        )

        return format_object_summary(
            self, self._formatter_func, is_justify=is_justify, name=name
        )
