    def _setitem_single_column(self, loc: int, value, plane_indexer):
        """

        Parameters
        ----------
        loc : int
            Indexer for column position
        plane_indexer : int, slice, listlike[int]
            The indexer we use for setitem along axis=0.
        """
        pi = plane_indexer

        orig_values = self.obj._get_column_array(loc)

        # perform the equivalent of a setitem on the info axis
        # as we have a null slice or a slice with full bounds
        # which means essentially reassign to the columns of a
        # multi-dim object
        # GH#6149 (null slice), GH#10408 (full bounds)
        if com.is_null_slice(pi) or com.is_full_slice(pi, len(self.obj)):
            pass
        elif (
            is_array_like(value)
            and len(value.shape) > 0
            and self.obj.shape[0] == value.shape[0]
            and not is_empty_indexer(pi)
        ):
            if is_list_like(pi):
                value = value[np.argsort(pi)]
            else:
                # in case of slice
                value = value[pi]
        else:
            # set value into the column (first attempting to operate inplace, then
            #  falling back to casting if necessary)
            self.obj._mgr.column_setitem(loc, plane_indexer, value)
            self.obj._clear_item_cache()
            return

        self.obj._iset_item(loc, value)

        # We will not operate in-place, but will attempt to in the future.
        #  To determine whether we need to issue a FutureWarning, see if the
        #  setting in-place would work, i.e. behavior will change.

        new_values = self.obj._get_column_array(loc)

        if can_hold_element(orig_values, new_values):
            # Don't issue the warning yet, as we can still trim a few cases where
            #  behavior will not change.

            if (
                isinstance(new_values, np.ndarray)
                and isinstance(orig_values, np.ndarray)
                and (
                    np.shares_memory(new_values, orig_values)
                    or new_values.shape != orig_values.shape
                )
            ):
                # TODO: get something like tm.shares_memory working?
                # The values were set inplace after all, no need to warn,
                #  e.g. test_rename_nocopy
                # In case of enlarging we can not set inplace, so need to
                # warn either
                pass
            else:
                warnings.warn(
                    "In a future version, `df.iloc[:, i] = newvals` will attempt "
                    "to set the values inplace instead of always setting a new "
                    "array. To retain the old behavior, use either "
                    "`df[df.columns[i]] = newvals` or, if columns are non-unique, "
                    "`df.isetitem(i, newvals)`",
                    FutureWarning,
                    stacklevel=find_stack_level(inspect.currentframe()),
                )
                # TODO: how to get future behavior?
                # TODO: what if we got here indirectly via loc?
        return
