    def column_setitem(
        self, loc: int, idx: int | slice | np.ndarray, value, inplace_only: bool = False
    ) -> None:
        """
        Set values ("setitem") into a single column (not setting the full column).

        This is a method on the ArrayManager level, to avoid creating an
        intermediate Series at the DataFrame level (`s = df[loc]; s[idx] = value`)
        """
        if not is_integer(loc):
            raise TypeError("The column index should be an integer")
        arr = self.arrays[loc]
        mgr = SingleArrayManager([arr], [self._axes[0]])
        if inplace_only:
            mgr.setitem_inplace(idx, value)
        else:
            new_mgr = mgr.setitem((idx,), value)
            # update existing ArrayManager in-place
            self.arrays[loc] = new_mgr.arrays[0]
