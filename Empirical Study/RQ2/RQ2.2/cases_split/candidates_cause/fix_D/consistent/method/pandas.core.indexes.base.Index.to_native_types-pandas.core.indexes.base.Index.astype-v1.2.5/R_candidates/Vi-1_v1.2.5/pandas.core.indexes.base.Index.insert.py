    def insert(self, loc: int, item):
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
        arr = np.asarray(self)
        item = self._coerce_scalar_to_index(item)._values
        idx = np.concatenate((arr[:loc], item, arr[loc:]))
        return Index(idx, name=self.name)
