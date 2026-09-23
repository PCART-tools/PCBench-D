    def _repr_categories(self):
        """ return the base repr for the categories """
        max_categories = (10 if get_option("display.max_categories") == 0
                    else get_option("display.max_categories"))
        from pandas.core import format as fmt
        category_strs = fmt.format_array(self.categories.get_values(), None)
        if len(category_strs) > max_categories:
            num = max_categories // 2
            head = category_strs[:num]
            tail = category_strs[-(max_categories - num):]
            category_strs = head + ["..."] + tail

        # Strip all leading spaces, which format_array adds for columns...
        category_strs = [x.strip() for x in category_strs]
        return category_strs
