    def _concat(self, to_concat: List["Index"], name: Label) -> "Index":
        """
        Concatenate multiple Index objects.
        """
        to_concat_vals = [x._values for x in to_concat]

        result = concat_compat(to_concat_vals)
        return Index(result, name=name)
