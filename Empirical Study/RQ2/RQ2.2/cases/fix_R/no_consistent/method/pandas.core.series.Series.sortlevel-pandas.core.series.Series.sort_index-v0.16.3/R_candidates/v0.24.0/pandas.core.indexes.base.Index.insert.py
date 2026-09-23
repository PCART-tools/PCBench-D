    def insert(self, loc, item):
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
        _self = np.asarray(self)
        item = self._coerce_scalar_to_index(item)._ndarray_values
        idx = np.concatenate((_self[:loc], item, _self[loc:]))
        return self._shallow_copy_with_infer(idx)
