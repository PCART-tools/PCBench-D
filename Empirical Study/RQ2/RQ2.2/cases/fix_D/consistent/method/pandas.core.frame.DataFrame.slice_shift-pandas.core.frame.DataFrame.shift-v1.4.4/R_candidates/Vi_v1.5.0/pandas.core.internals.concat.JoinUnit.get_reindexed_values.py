    def get_reindexed_values(self, empty_dtype: DtypeObj, upcasted_na) -> ArrayLike:
        values: ArrayLike

        if upcasted_na is None and self.block.dtype.kind != "V":
            # No upcasting is necessary
            fill_value = self.block.fill_value
            values = self.block.get_values()
        else:
            fill_value = upcasted_na

            if self._is_valid_na_for(empty_dtype):
                # note: always holds when self.block.dtype.kind == "V"
                blk_dtype = self.block.dtype

                if blk_dtype == np.dtype("object"):
                    # we want to avoid filling with np.nan if we are
                    # using None; we already know that we are all
                    # nulls
                    values = self.block.values.ravel(order="K")
                    if len(values) and values[0] is None:
                        fill_value = None

                if isinstance(empty_dtype, DatetimeTZDtype):
                    # NB: exclude e.g. pyarrow[dt64tz] dtypes
                    i8values = np.full(self.shape, fill_value.value)
                    return DatetimeArray(i8values, dtype=empty_dtype)

                elif is_1d_only_ea_dtype(empty_dtype):
                    if is_dtype_equal(blk_dtype, empty_dtype) and self.indexers:
                        # avoid creating new empty array if we already have an array
                        # with correct dtype that can be reindexed
                        pass
                    else:
                        empty_dtype = cast(ExtensionDtype, empty_dtype)
                        cls = empty_dtype.construct_array_type()

                        missing_arr = cls._from_sequence([], dtype=empty_dtype)
                        ncols, nrows = self.shape
                        assert ncols == 1, ncols
                        empty_arr = -1 * np.ones((nrows,), dtype=np.intp)
                        return missing_arr.take(
                            empty_arr, allow_fill=True, fill_value=fill_value
                        )
                elif isinstance(empty_dtype, ExtensionDtype):
                    # TODO: no tests get here, a handful would if we disabled
                    #  the dt64tz special-case above (which is faster)
                    cls = empty_dtype.construct_array_type()
                    missing_arr = cls._empty(shape=self.shape, dtype=empty_dtype)
                    missing_arr[:] = fill_value
                    return missing_arr
                else:
                    # NB: we should never get here with empty_dtype integer or bool;
                    #  if we did, the missing_arr.fill would cast to gibberish
                    missing_arr = np.empty(self.shape, dtype=empty_dtype)
                    missing_arr.fill(fill_value)
                    return missing_arr

            if (not self.indexers) and (not self.block._can_consolidate):
                # preserve these for validation in concat_compat
                return self.block.values

            if self.block.is_bool:
                # External code requested filling/upcasting, bool values must
                # be upcasted to object to avoid being upcasted to numeric.
                values = self.block.astype(np.dtype("object")).values
            else:
                # No dtype upcasting is done here, it will be performed during
                # concatenation itself.
                values = self.block.values

        if not self.indexers:
            # If there's no indexing to be done, we want to signal outside
            # code that this array must be copied explicitly.  This is done
            # by returning a view and checking `retval.base`.
            values = values.view()

        else:
            for ax, indexer in self.indexers.items():
                values = algos.take_nd(values, indexer, axis=ax)

        return values
