    def _format_attrs(self):
        """
        Return a list of tuples of the (attr,formatted_value)
        """
        max_categories = (
            10
            if get_option("display.max_categories") == 0
            else get_option("display.max_categories")
        )
        attrs = [
            (
                "categories",
                ibase.default_pprint(self.categories, max_seq_items=max_categories),
            ),
            # error: "CategoricalIndex" has no attribute "ordered"
            ("ordered", self.ordered),  # type: ignore[attr-defined]
        ]
        extra = super()._format_attrs()
        return attrs + extra
