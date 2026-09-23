    def insert(self, loc: int, item):
        """
        Make new Index inserting new item at location. Follows
        Python list.append semantics for negative values.

        Parameters
        ----------
        loc : int
        item : object

        Returns
        -------
        new_index : Index

        Raises
        ------
        ValueError if the item is not valid for this dtype.
        """
        arr = self._data
        code = arr._validate_scalar(item)

        new_vals = np.concatenate((arr._ndarray[:loc], [code], arr._ndarray[loc:]))
        new_arr = arr._from_backing_data(new_vals)
        return type(self)._simple_new(new_arr, name=self.name)
