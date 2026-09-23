    def insert(self, loc: int, item) -> Index:
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
        """
        try:
            result = self._data.insert(loc, item)
        except (ValueError, TypeError):
            # e.g. trying to insert an integer into a DatetimeIndex
            #  We cannot keep the same dtype, so cast to the (often object)
            #  minimal shared dtype before doing the insert.
            dtype = self._find_common_type_compat(item)
            return self.astype(dtype).insert(loc, item)
        else:
            return type(self)._simple_new(result, name=self.name)
