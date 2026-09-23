    @cache_readonly
    def _hash_categories(self) -> int:
        from pandas.core.util.hashing import (
            combine_hash_arrays,
            hash_array,
            hash_tuples,
        )

        categories = self.categories
        ordered = self.ordered

        if len(categories) and isinstance(categories[0], tuple):
            # assumes if any individual category is a tuple, then all our. ATM
            # I don't really want to support just some of the categories being
            # tuples.
            cat_list = list(categories)  # breaks if a np.array of categories
            cat_array = hash_tuples(cat_list)
        else:
            if categories.dtype == "O" and len({type(x) for x in categories}) != 1:
                # TODO: hash_array doesn't handle mixed types. It casts
                # everything to a str first, which means we treat
                # {'1', '2'} the same as {'1', 2}
                # find a better solution
                hashed = hash((tuple(categories), ordered))
                return hashed

            if DatetimeTZDtype.is_dtype(categories.dtype):
                # Avoid future warning.
                categories = categories.view("datetime64[ns]")

            cat_array = hash_array(np.asarray(categories), categorize=False)
        if ordered:
            cat_array = np.vstack(
                [cat_array, np.arange(len(cat_array), dtype=cat_array.dtype)]
            )
        else:
            cat_array = np.array([cat_array])
        combined_hashed = combine_hash_arrays(iter(cat_array), num_items=len(cat_array))
        return np.bitwise_xor.reduce(combined_hashed)
