    def _concat(self, to_concat: list[Index], name: Hashable) -> Index:
        """
        Concatenate multiple Index objects.
        """
        to_concat_vals = [x._values for x in to_concat]

        result = concat_compat(to_concat_vals)

        is_numeric = result.dtype.kind in ["i", "u", "f"]
        if self._is_backward_compat_public_numeric_index and is_numeric:
            return type(self)._simple_new(result, name=name)

        return Index._with_infer(result, name=name)
