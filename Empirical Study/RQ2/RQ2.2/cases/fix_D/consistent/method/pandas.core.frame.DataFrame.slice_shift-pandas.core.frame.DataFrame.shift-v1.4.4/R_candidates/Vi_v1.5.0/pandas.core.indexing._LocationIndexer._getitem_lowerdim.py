    @final
    def _getitem_lowerdim(self, tup: tuple):

        # we can directly get the axis result since the axis is specified
        if self.axis is not None:
            axis = self.obj._get_axis_number(self.axis)
            return self._getitem_axis(tup, axis=axis)

        # we may have a nested tuples indexer here
        if self._is_nested_tuple_indexer(tup):
            return self._getitem_nested_tuple(tup)

        # we maybe be using a tuple to represent multiple dimensions here
        ax0 = self.obj._get_axis(0)
        # ...but iloc should handle the tuple as simple integer-location
        # instead of checking it as multiindex representation (GH 13797)
        if (
            isinstance(ax0, MultiIndex)
            and self.name != "iloc"
            and not any(isinstance(x, slice) for x in tup)
        ):
            # Note: in all extant test cases, replacing the slice condition with
            #  `all(is_hashable(x) or com.is_null_slice(x) for x in tup)`
            #  is equivalent.
            #  (see the other place where we call _handle_lowerdim_multi_index_axis0)
            with suppress(IndexingError):
                # error "_LocationIndexer" has no attribute
                # "_handle_lowerdim_multi_index_axis0"
                return cast(_LocIndexer, self)._handle_lowerdim_multi_index_axis0(tup)

        tup = self._validate_key_length(tup)

        for i, key in enumerate(tup):
            if is_label_like(key):
                # We don't need to check for tuples here because those are
                #  caught by the _is_nested_tuple_indexer check above.
                section = self._getitem_axis(key, axis=i)

                # We should never have a scalar section here, because
                #  _getitem_lowerdim is only called after a check for
                #  is_scalar_access, which that would be.
                if section.ndim == self.ndim:
                    # we're in the middle of slicing through a MultiIndex
                    # revise the key wrt to `section` by inserting an _NS
                    new_key = tup[:i] + (_NS,) + tup[i + 1 :]

                else:
                    # Note: the section.ndim == self.ndim check above
                    #  rules out having DataFrame here, so we dont need to worry
                    #  about transposing.
                    new_key = tup[:i] + tup[i + 1 :]

                    if len(new_key) == 1:
                        new_key = new_key[0]

                # Slices should return views, but calling iloc/loc with a null
                # slice returns a new object.
                if com.is_null_slice(new_key):
                    return section
                # This is an elided recursive call to iloc/loc
                return getattr(section, self.name)[new_key]

        raise IndexingError("not applicable")
