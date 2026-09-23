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
            # pandas\core\indexes\category.py:315: error: "CategoricalIndex"
            # has no attribute "ordered"  [attr-defined]
            ("ordered", self.ordered),  # type: ignore[attr-defined]
        ]
        if self.name is not None:
            attrs.append(("name", ibase.default_pprint(self.name)))
        attrs.append(("dtype", f"'{self.dtype.name}'"))
        max_seq_items = get_option("display.max_seq_items") or len(self)
        if len(self) > max_seq_items:
            attrs.append(("length", len(self)))
        return attrs
