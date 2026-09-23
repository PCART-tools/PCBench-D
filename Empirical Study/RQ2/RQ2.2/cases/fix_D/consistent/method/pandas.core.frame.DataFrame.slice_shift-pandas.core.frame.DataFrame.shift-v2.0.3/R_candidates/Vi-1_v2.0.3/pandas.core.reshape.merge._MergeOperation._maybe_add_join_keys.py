    def _maybe_add_join_keys(
        self,
        result: DataFrame,
        left_indexer: np.ndarray | None,
        right_indexer: np.ndarray | None,
    ) -> None:
        left_has_missing = None
        right_has_missing = None

        assert all(is_array_like(x) for x in self.left_join_keys)

        keys = zip(self.join_names, self.left_on, self.right_on)
        for i, (name, lname, rname) in enumerate(keys):
            if not _should_fill(lname, rname):
                continue

            take_left, take_right = None, None

            if name in result:
                if left_indexer is not None and right_indexer is not None:
                    if name in self.left:
                        if left_has_missing is None:
                            left_has_missing = (left_indexer == -1).any()

                        if left_has_missing:
                            take_right = self.right_join_keys[i]

                            if not is_dtype_equal(
                                result[name].dtype, self.left[name].dtype
                            ):
                                take_left = self.left[name]._values

                    elif name in self.right:
                        if right_has_missing is None:
                            right_has_missing = (right_indexer == -1).any()

                        if right_has_missing:
                            take_left = self.left_join_keys[i]

                            if not is_dtype_equal(
                                result[name].dtype, self.right[name].dtype
                            ):
                                take_right = self.right[name]._values

            elif left_indexer is not None:
                take_left = self.left_join_keys[i]
                take_right = self.right_join_keys[i]

            if take_left is not None or take_right is not None:
                if take_left is None:
                    lvals = result[name]._values
                else:
                    # TODO: can we pin down take_left's type earlier?
                    take_left = extract_array(take_left, extract_numpy=True)
                    lfill = na_value_for_dtype(take_left.dtype)
                    lvals = algos.take_nd(take_left, left_indexer, fill_value=lfill)

                if take_right is None:
                    rvals = result[name]._values
                else:
                    # TODO: can we pin down take_right's type earlier?
                    taker = extract_array(take_right, extract_numpy=True)
                    rfill = na_value_for_dtype(taker.dtype)
                    rvals = algos.take_nd(taker, right_indexer, fill_value=rfill)

                # if we have an all missing left_indexer
                # make sure to just use the right values or vice-versa
                mask_left = left_indexer == -1
                # error: Item "bool" of "Union[Any, bool]" has no attribute "all"
                if mask_left.all():  # type: ignore[union-attr]
                    key_col = Index(rvals)
                    result_dtype = rvals.dtype
                elif right_indexer is not None and (right_indexer == -1).all():
                    key_col = Index(lvals)
                    result_dtype = lvals.dtype
                else:
                    key_col = Index(lvals).where(~mask_left, rvals)
                    result_dtype = find_common_type([lvals.dtype, rvals.dtype])
                    if (
                        lvals.dtype.kind == "M"
                        and rvals.dtype.kind == "M"
                        and result_dtype.kind == "O"
                    ):
                        # TODO(non-nano) Workaround for common_type not dealing
                        # with different resolutions
                        result_dtype = key_col.dtype

                if result._is_label_reference(name):
                    result[name] = Series(
                        key_col, dtype=result_dtype, index=result.index
                    )
                elif result._is_level_reference(name):
                    if isinstance(result.index, MultiIndex):
                        key_col.name = name
                        idx_list = [
                            result.index.get_level_values(level_name)
                            if level_name != name
                            else key_col
                            for level_name in result.index.names
                        ]

                        result.set_index(idx_list, inplace=True)
                    else:
                        result.index = Index(key_col, name=name)
                else:
                    result.insert(i, name or f"key_{i}", key_col)
