    def _hash_categorical(c, encoding, hash_key):
        cat_hashed = hash_array(c.categories.values, encoding, hash_key,
                                categorize=False).astype(np.uint64, copy=False)
        return c.rename_categories(cat_hashed).astype(np.uint64)
