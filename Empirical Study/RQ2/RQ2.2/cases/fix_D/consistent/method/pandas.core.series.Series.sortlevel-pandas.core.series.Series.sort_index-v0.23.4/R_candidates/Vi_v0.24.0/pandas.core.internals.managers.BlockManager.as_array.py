    def as_array(self, transpose=False, items=None):
        """Convert the blockmanager data into an numpy array.

        Parameters
        ----------
        transpose : boolean, default False
            If True, transpose the return array
        items : list of strings or None
            Names of block items that will be included in the returned
            array. ``None`` means that all block items will be used

        Returns
        -------
        arr : ndarray
        """
        if len(self.blocks) == 0:
            arr = np.empty(self.shape, dtype=float)
            return arr.transpose() if transpose else arr

        if items is not None:
            mgr = self.reindex_axis(items, axis=0)
        else:
            mgr = self

        if self._is_single_block and mgr.blocks[0].is_datetimetz:
            # TODO(Block.get_values): Make DatetimeTZBlock.get_values
            # always be object dtype. Some callers seem to want the
            # DatetimeArray (previously DTI)
            arr = mgr.blocks[0].get_values(dtype=object)
        elif self._is_single_block or not self.is_mixed_type:
            arr = np.asarray(mgr.blocks[0].get_values())
        else:
            arr = mgr._interleave()

        return arr.transpose() if transpose else arr
