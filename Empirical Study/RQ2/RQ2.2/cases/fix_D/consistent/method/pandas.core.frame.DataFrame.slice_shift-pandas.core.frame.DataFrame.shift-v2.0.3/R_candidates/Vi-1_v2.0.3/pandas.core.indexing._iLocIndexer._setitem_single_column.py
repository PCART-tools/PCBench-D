    def _setitem_single_column(self, loc: int, value, plane_indexer) -> None:
        """

        Parameters
        ----------
        loc : int
            Indexer for column position
        plane_indexer : int, slice, listlike[int]
            The indexer we use for setitem along axis=0.
        """
        pi = plane_indexer

        is_full_setter = com.is_null_slice(pi) or com.is_full_slice(pi, len(self.obj))

        is_null_setter = com.is_empty_slice(pi) or is_array_like(pi) and len(pi) == 0

        if is_null_setter:
            # no-op, don't cast dtype later
            return

        elif is_full_setter:
            try:
                self.obj._mgr.column_setitem(
                    loc, plane_indexer, value, inplace_only=True
                )
            except (ValueError, TypeError, LossySetitemError):
                # If we're setting an entire column and we can't do it inplace,
                #  then we can use value's dtype (or inferred dtype)
                #  instead of object
                self.obj.isetitem(loc, value)
        else:
            # set value into the column (first attempting to operate inplace, then
            #  falling back to casting if necessary)
            self.obj._mgr.column_setitem(loc, plane_indexer, value)

        self.obj._clear_item_cache()
