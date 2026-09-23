    def _repr_categories(self):
        """
        return the base repr for the categories
        """
        max_categories = (
            10
            if get_option("display.max_categories") == 0
            else get_option("display.max_categories")
        )
        from pandas.io.formats import format as fmt

        if len(self.categories) > max_categories:
            num = max_categories // 2
            head = fmt.format_array(self.categories[:num], None)
            tail = fmt.format_array(self.categories[-num:], None)
            category_strs = head + ["..."] + tail
        else:
            category_strs = fmt.format_array(self.categories, None)

        # Strip all leading spaces, which format_array adds for columns...
        category_strs = [x.strip() for x in category_strs]
        return category_strs
