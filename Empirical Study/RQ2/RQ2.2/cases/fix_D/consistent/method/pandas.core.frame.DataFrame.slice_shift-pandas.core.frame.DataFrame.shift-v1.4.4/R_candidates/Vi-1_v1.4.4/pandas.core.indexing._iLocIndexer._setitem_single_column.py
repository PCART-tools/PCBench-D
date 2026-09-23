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

        ser = self.obj._ixs(loc, axis=1)

        # perform the equivalent of a setitem on the info axis
        # as we have a null slice or a slice with full bounds
        # which means essentially reassign to the columns of a
        # multi-dim object
        # GH#6149 (null slice), GH#10408 (full bounds)
        if com.is_null_slice(pi) or com.is_full_slice(pi, len(self.obj)):
            ser = value
        elif (
            is_array_like(value)
            and is_exact_shape_match(ser, value)
            and not is_empty_indexer(pi, value)
        ):
            if is_list_like(pi):
                ser = value[np.argsort(pi)]
            else:
                # in case of slice
                ser = value[pi]
        else:
            # set the item, first attempting to operate inplace, then
            #  falling back to casting if necessary; see
            #  _whatsnew_130.notable_bug_fixes.setitem_column_try_inplace

            orig_values = ser._values
            ser._mgr = ser._mgr.setitem((pi,), value)

            if ser._values is orig_values:
                # The setitem happened inplace, so the DataFrame's values
                #  were modified inplace.
                return
            self.obj._iset_item(loc, ser)
            return

        # reset the sliced object if unique
        self.obj._iset_item(loc, ser)
