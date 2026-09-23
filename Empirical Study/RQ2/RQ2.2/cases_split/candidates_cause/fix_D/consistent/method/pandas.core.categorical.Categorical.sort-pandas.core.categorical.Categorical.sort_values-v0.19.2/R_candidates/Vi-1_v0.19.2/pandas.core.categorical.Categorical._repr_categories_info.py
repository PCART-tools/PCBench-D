    def _repr_categories_info(self):
        """ Returns a string representation of the footer."""

        category_strs = self._repr_categories()
        dtype = getattr(self.categories, 'dtype_str',
                        str(self.categories.dtype))

        levheader = "Categories (%d, %s): " % (len(self.categories), dtype)
        width, height = get_terminal_size()
        max_width = get_option("display.width") or width
        if com.in_ipython_frontend():
            # 0 = no breaks
            max_width = 0
        levstring = ""
        start = True
        cur_col_len = len(levheader)  # header
        sep_len, sep = (3, " < ") if self.ordered else (2, ", ")
        linesep = sep.rstrip() + "\n"  # remove whitespace
        for val in category_strs:
            if max_width != 0 and cur_col_len + sep_len + len(val) > max_width:
                levstring += linesep + (" " * (len(levheader) + 1))
                cur_col_len = len(levheader) + 1  # header + a whitespace
            elif not start:
                levstring += sep
                cur_col_len += len(val)
            levstring += val
            start = False
        # replace to simple save space by
        return levheader + "[" + levstring.replace(" < ... < ", " ... ") + "]"
