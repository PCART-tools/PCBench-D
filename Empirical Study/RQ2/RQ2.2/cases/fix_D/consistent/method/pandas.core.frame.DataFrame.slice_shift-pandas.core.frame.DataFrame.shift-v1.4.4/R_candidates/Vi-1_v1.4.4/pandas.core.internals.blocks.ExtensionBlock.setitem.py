    def setitem(self, indexer, value):
        """
        Attempt self.values[indexer] = value, possibly creating a new array.

        This differs from Block.setitem by not allowing setitem to change
        the dtype of the Block.

        Parameters
        ----------
        indexer : tuple, list-like, array-like, slice, int
            The subset of self.values to set
        value : object
            The value being set

        Returns
        -------
        Block

        Notes
        -----
        `indexer` is a direct slice/positional indexer. `value` must
        be a compatible shape.
        """
        if not self._can_hold_element(value):
            # see TestSetitemFloatIntervalWithIntIntervalValues
            return self.coerce_to_target_dtype(value).setitem(indexer, value)

        if isinstance(indexer, tuple):
            # TODO(EA2D): not needed with 2D EAs
            # we are always 1-D
            indexer = indexer[0]
            if isinstance(indexer, np.ndarray) and indexer.ndim == 2:
                # GH#44703
                if indexer.shape[1] != 1:
                    raise NotImplementedError(
                        "This should not be reached. Please report a bug at "
                        "github.com/pandas-dev/pandas/"
                    )
                indexer = indexer[:, 0]

        # TODO(EA2D): not needed with 2D EAS
        if isinstance(value, (np.ndarray, ExtensionArray)) and value.ndim == 2:
            assert value.shape[1] == 1
            # error: No overload variant of "__getitem__" of "ExtensionArray"
            # matches argument type "Tuple[slice, int]"
            value = value[:, 0]  # type: ignore[call-overload]
        elif isinstance(value, ABCDataFrame):
            # TODO: should we avoid getting here with DataFrame?
            assert value.shape[1] == 1
            value = value._ixs(0, axis=1)._values

        check_setitem_lengths(indexer, value, self.values)
        self.values[indexer] = value
        return self
