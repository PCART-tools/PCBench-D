    def _format_attrs(self) -> list[tuple[str_t, str_t | int | bool | None]]:
        """
        Return a list of tuples of the (attr,formatted_value).
        """
        attrs: list[tuple[str_t, str_t | int | bool | None]] = []

        if not self._is_multi:
            attrs.append(("dtype", f"'{self.dtype}'"))

        if self.name is not None:
            attrs.append(("name", default_pprint(self.name)))
        elif self._is_multi and any(x is not None for x in self.names):
            attrs.append(("names", default_pprint(self.names)))

        max_seq_items = get_option("display.max_seq_items") or len(self)
        if len(self) > max_seq_items:
            attrs.append(("length", len(self)))
        return attrs
