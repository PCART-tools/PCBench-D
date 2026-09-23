    def _format_attrs(self):
        """
        Return a list of tuples of the (attr,formatted_value)
        """
        max_categories = (
            10
            if get_option("display.max_categories") == 0
            else get_option("display.max_categories")
        )
        attrs: list[tuple[str, str | int | bool | None]]
        attrs = [
            (
                "categories",
                ibase.default_pprint(self.categories, max_seq_items=max_categories),
            ),
            ("ordered", self.ordered),
        ]
        extra = super()._format_attrs()
        return attrs + extra
