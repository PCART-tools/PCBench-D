    def _format_data(self, name=None) -> str_t:
        """
        Return the formatted data as a unicode string.
        """
        # do we want to justify (only do so for non-objects)
        is_justify = True

        if self.inferred_type == "string":
            is_justify = False
        elif self.inferred_type == "categorical":
            # error: "Index" has no attribute "categories"
            if is_object_dtype(self.categories):  # type: ignore[attr-defined]
                is_justify = False

        return format_object_summary(
            self, self._formatter_func, is_justify=is_justify, name=name
        )
