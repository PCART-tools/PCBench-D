    def _repr_categories_info(self):
        """ Returns a string representation of the footer."""

        max_categories = (10 if get_option("display.max_categories") == 0
                    else get_option("display.max_categories"))
        category_strs = fmt.format_array(self.categories.get_values(), None)
        if len(category_strs) > max_categories:
            num = max_categories // 2
            head = category_strs[:num]
            tail = category_strs[-(max_categories - num):]
            category_strs = head + ["..."] + tail
        # Strip all leading spaces, which format_array adds for columns...
        category_strs = [x.strip() for x in category_strs]
        levheader = "Categories (%d, %s): " % (len(self.categories),
                                               self.categories.dtype)
        width, height = get_terminal_size()
        max_width = (width if get_option("display.width") == 0
                    else get_option("display.width"))
        if com.in_ipython_frontend():
            # 0 = no breaks
            max_width = 0
        levstring = ""
        start = True
        cur_col_len = len(levheader)
        sep_len, sep = (3, " < ") if self.ordered else (2, ", ")
        for val in category_strs:
            if max_width != 0 and cur_col_len + sep_len + len(val) > max_width:
                levstring += "\n" + (" "* len(levheader))
                cur_col_len = len(levheader)
            if not start:
                levstring += sep
                cur_col_len += len(val)
            levstring += val
            start = False
        # replace to simple save space by
        return levheader + "["+levstring.replace(" < ... < ", " ... ")+"]"
