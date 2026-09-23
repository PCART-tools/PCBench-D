    def _format_attrs(self) -> list[tuple[str_t, str_t | int]]:
        """
        Return a list of tuples of the (attr,formatted_value).
        """
        return format_object_attrs(self, include_dtype=not self._is_multi)
