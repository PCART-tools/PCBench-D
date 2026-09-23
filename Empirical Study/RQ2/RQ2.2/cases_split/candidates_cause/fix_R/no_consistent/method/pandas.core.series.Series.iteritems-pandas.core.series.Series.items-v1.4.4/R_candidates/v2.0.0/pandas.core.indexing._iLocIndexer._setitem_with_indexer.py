    def _setitem_with_indexer(self, indexer, value, name: str = "iloc"):
        """
        _setitem_with_indexer is for setting values on a Series/DataFrame
        using positional indexers.

        If the relevant keys are not present, the Series/DataFrame may be
        expanded.

        This method is currently broken when dealing with non-unique Indexes,
        since it goes from positional indexers back to labels when calling
        BlockManager methods, see GH#12991, GH#22046, GH#15686.
        """
        info_axis = self.obj._info_axis_number

        # maybe partial set
        take_split_path = not self.obj._mgr.is_single_block

        if not take_split_path and isinstance(value, ABCDataFrame):
            # Avoid cast of values
            take_split_path = not value._mgr.is_single_block

        # if there is only one block/type, still have to take split path
        # unless the block is one-dimensional or it can hold the value
        if not take_split_path and len(self.obj._mgr.arrays) and self.ndim > 1:
            # in case of dict, keys are indices
            val = list(value.values()) if isinstance(value, dict) else value
            arr = self.obj._mgr.arrays[0]
            take_split_path = not can_hold_element(
                arr, extract_array(val, extract_numpy=True)
            )

        # if we have any multi-indexes that have non-trivial slices
        # (not null slices) then we must take the split path, xref
        # GH 10360, GH 27841
        if isinstance(indexer, tuple) and len(indexer) == len(self.obj.axes):
            for i, ax in zip(indexer, self.obj.axes):
                if isinstance(ax, MultiIndex) and not (
                    is_integer(i) or com.is_null_slice(i)
                ):
                    take_split_path = True
                    break

        if isinstance(indexer, tuple):
            nindexer = []
            for i, idx in enumerate(indexer):
                if isinstance(idx, dict):
                    # reindex the axis to the new value
                    # and set inplace
                    key, _ = convert_missing_indexer(idx)

                    # if this is the items axes, then take the main missing
                    # path first
                    # this correctly sets the dtype and avoids cache issues
                    # essentially this separates out the block that is needed
                    # to possibly be modified
                    if self.ndim > 1 and i == info_axis:
                        # add the new item, and set the value
                        # must have all defined axes if we have a scalar
                        # or a list-like on the non-info axes if we have a
                        # list-like
                        if not len(self.obj):
                            if not is_list_like_indexer(value):
                                raise ValueError(
                                    "cannot set a frame with no "
                                    "defined index and a scalar"
                                )
                            self.obj[key] = value
                            return

                        # add a new item with the dtype setup
                        if com.is_null_slice(indexer[0]):
                            # We are setting an entire column
                            self.obj[key] = value
                            return
                        elif is_array_like(value):
                            # GH#42099
                            arr = extract_array(value, extract_numpy=True)
                            taker = -1 * np.ones(len(self.obj), dtype=np.intp)
                            empty_value = algos.take_nd(arr, taker)
                            if not isinstance(value, ABCSeries):
                                # if not Series (in which case we need to align),
                                #  we can short-circuit
                                empty_value[indexer[0]] = arr
                                self.obj[key] = empty_value
                                return

                            self.obj[key] = empty_value

                        else:
                            # FIXME: GH#42099#issuecomment-864326014
                            self.obj[key] = infer_fill_value(value)

                        new_indexer = convert_from_missing_indexer_tuple(
                            indexer, self.obj.axes
                        )
                        self._setitem_with_indexer(new_indexer, value, name)

                        return

                    # reindex the axis
                    # make sure to clear the cache because we are
                    # just replacing the block manager here
                    # so the object is the same
                    index = self.obj._get_axis(i)
                    labels = index.insert(len(index), key)

                    # We are expanding the Series/DataFrame values to match
                    #  the length of thenew index `labels`.  GH#40096 ensure
                    #  this is valid even if the index has duplicates.
                    taker = np.arange(len(index) + 1, dtype=np.intp)
                    taker[-1] = -1
                    reindexers = {i: (labels, taker)}
                    new_obj = self.obj._reindex_with_indexers(
                        reindexers, allow_dups=True
                    )
                    self.obj._mgr = new_obj._mgr
                    self.obj._maybe_update_cacher(clear=True)
                    self.obj._is_copy = None

                    nindexer.append(labels.get_loc(key))

                else:
                    nindexer.append(idx)

            indexer = tuple(nindexer)
        else:
            indexer, missing = convert_missing_indexer(indexer)

            if missing:
                self._setitem_with_indexer_missing(indexer, value)
                return

        if name == "loc":
            # must come after setting of missing
            indexer, value = self._maybe_mask_setitem_value(indexer, value)

        # align and set the values
        if take_split_path:
            # We have to operate column-wise
            self._setitem_with_indexer_split_path(indexer, value, name)
        else:
            self._setitem_single_block(indexer, value, name)
