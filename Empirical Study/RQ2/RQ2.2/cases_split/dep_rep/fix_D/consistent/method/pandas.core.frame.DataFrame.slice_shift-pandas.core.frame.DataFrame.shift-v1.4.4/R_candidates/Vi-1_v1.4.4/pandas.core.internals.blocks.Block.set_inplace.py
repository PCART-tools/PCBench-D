    def set_inplace(self, locs, values) -> None:
        """
        Modify block values in-place with new item value.

        Notes
        -----
        `set` never creates a new array or new Block, whereas `setitem` _may_
        create a new array and always creates a new Block.
        """
        self.values[locs] = values
