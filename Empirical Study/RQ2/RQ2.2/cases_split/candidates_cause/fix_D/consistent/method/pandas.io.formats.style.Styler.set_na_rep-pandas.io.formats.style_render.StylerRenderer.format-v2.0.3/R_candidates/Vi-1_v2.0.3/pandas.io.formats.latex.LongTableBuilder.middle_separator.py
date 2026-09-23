    @property
    def middle_separator(self) -> str:
        iterator = self._create_row_iterator(over="header")

        # the content between \endfirsthead and \endhead commands
        # mitigates repeated List of Tables entries in the final LaTeX
        # document when dealing with longtable environments; GH #34360
        elements = [
            "\\midrule",
            "\\endfirsthead",
            f"\\caption[]{{{self.caption}}} \\\\" if self.caption else "",
            self.top_separator,
            self.header,
            "\\midrule",
            "\\endhead",
            "\\midrule",
            f"\\multicolumn{{{len(iterator.strcols)}}}{{r}}"
            "{{Continued on next page}} \\\\",
            "\\midrule",
            "\\endfoot\n",
            "\\bottomrule",
            "\\endlastfoot",
        ]
        if self._is_separator_required():
            return "\n".join(elements)
        return ""
