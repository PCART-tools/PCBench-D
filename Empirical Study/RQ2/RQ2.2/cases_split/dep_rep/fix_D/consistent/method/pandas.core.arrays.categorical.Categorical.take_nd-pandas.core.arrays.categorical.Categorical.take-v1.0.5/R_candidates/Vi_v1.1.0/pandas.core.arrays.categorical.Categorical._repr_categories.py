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

        format_array = partial(
            fmt.format_array, formatter=None, quoting=QUOTE_NONNUMERIC
        )
        if len(self.categories) > max_categories:
            num = max_categories // 2
            head = format_array(self.categories[:num])
            tail = format_array(self.categories[-num:])
            category_strs = head + ["..."] + tail
        else:
            category_strs = format_array(self.categories)

        # Strip all leading spaces, which format_array adds for columns...
        category_strs = [x.strip() for x in category_strs]
        return category_strs
