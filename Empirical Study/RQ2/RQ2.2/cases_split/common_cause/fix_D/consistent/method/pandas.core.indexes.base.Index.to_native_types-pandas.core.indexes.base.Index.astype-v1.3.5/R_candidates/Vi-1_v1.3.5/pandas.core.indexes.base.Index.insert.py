    def insert(self, loc: int, item) -> Index:
        """
        Make new Index inserting new item at location.

        Follows Python list.append semantics for negative values.

        Parameters
        ----------
        loc : int
        item : object

        Returns
        -------
        new_index : Index
        """
        # Note: this method is overridden by all ExtensionIndex subclasses,
        #  so self is never backed by an EA.
        item = lib.item_from_zerodim(item)
        if is_valid_na_for_dtype(item, self.dtype) and self.dtype != object:
            item = self._na_value

        try:
            item = self._validate_fill_value(item)
        except TypeError:
            inferred, _ = infer_dtype_from(item)
            dtype = find_common_type([self.dtype, inferred])
            return self.astype(dtype).insert(loc, item)

        arr = np.asarray(self)

        # Use Index constructor to ensure we get tuples cast correctly.
        item = Index([item], dtype=self.dtype)._values
        idx = np.concatenate((arr[:loc], item, arr[loc:]))
        return Index(idx, name=self.name)
