    def insert(self: ExtensionArrayT, loc: int, item) -> ExtensionArrayT:
        """
        Insert an item at the given position.

        Parameters
        ----------
        loc : int
        item : scalar-like

        Returns
        -------
        same type as self

        Notes
        -----
        This method should be both type and dtype-preserving.  If the item
        cannot be held in an array of this type/dtype, either ValueError or
        TypeError should be raised.

        The default implementation relies on _from_sequence to raise on invalid
        items.
        """
        loc = validate_insert_loc(loc, len(self))

        item_arr = type(self)._from_sequence([item], dtype=self.dtype)

        return type(self)._concat_same_type([self[:loc], item_arr, self[loc:]])
