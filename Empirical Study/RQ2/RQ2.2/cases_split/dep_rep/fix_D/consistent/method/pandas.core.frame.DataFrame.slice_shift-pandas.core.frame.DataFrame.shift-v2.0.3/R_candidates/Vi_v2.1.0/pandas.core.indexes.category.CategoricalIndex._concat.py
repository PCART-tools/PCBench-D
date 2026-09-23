    def _concat(self, to_concat: list[Index], name: Hashable) -> Index:
        # if calling index is category, don't check dtype of others
        try:
            cat = Categorical._concat_same_type(
                [self._is_dtype_compat(c) for c in to_concat]
            )
        except TypeError:
            # not all to_concat elements are among our categories (or NA)

            res = concat_compat([x._values for x in to_concat])
            return Index(res, name=name)
        else:
            return type(self)._simple_new(cat, name=name)
