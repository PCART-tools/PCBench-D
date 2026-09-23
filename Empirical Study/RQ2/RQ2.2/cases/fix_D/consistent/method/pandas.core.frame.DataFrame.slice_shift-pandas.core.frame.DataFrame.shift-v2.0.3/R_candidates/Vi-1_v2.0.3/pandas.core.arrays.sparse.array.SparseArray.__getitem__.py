    def __getitem__(
        self: SparseArrayT,
        key: PositionalIndexer | tuple[int | ellipsis, ...],
    ) -> SparseArrayT | Any:
        if isinstance(key, tuple):
            key = unpack_tuple_and_ellipses(key)
            if key is Ellipsis:
                raise ValueError("Cannot slice with Ellipsis")

        if is_integer(key):
            return self._get_val_at(key)
        elif isinstance(key, tuple):
            # error: Invalid index type "Tuple[Union[int, ellipsis], ...]"
            # for "ndarray[Any, Any]"; expected type
            # "Union[SupportsIndex, _SupportsArray[dtype[Union[bool_,
            # integer[Any]]]], _NestedSequence[_SupportsArray[dtype[
            # Union[bool_, integer[Any]]]]], _NestedSequence[Union[
            # bool, int]], Tuple[Union[SupportsIndex, _SupportsArray[
            # dtype[Union[bool_, integer[Any]]]], _NestedSequence[
            # _SupportsArray[dtype[Union[bool_, integer[Any]]]]],
            # _NestedSequence[Union[bool, int]]], ...]]"
            data_slice = self.to_dense()[key]  # type: ignore[index]
        elif isinstance(key, slice):
            # Avoid densifying when handling contiguous slices
            if key.step is None or key.step == 1:
                start = 0 if key.start is None else key.start
                if start < 0:
                    start += len(self)

                end = len(self) if key.stop is None else key.stop
                if end < 0:
                    end += len(self)

                indices = self.sp_index.indices
                keep_inds = np.flatnonzero((indices >= start) & (indices < end))
                sp_vals = self.sp_values[keep_inds]

                sp_index = indices[keep_inds].copy()

                # If we've sliced to not include the start of the array, all our indices
                # should be shifted. NB: here we are careful to also not shift by a
                # negative value for a case like [0, 1][-100:] where the start index
                # should be treated like 0
                if start > 0:
                    sp_index -= start

                # Length of our result should match applying this slice to a range
                # of the length of our original array
                new_len = len(range(len(self))[key])
                new_sp_index = make_sparse_index(new_len, sp_index, self.kind)
                return type(self)._simple_new(sp_vals, new_sp_index, self.dtype)
            else:
                indices = np.arange(len(self), dtype=np.int32)[key]
                return self.take(indices)

        elif not is_list_like(key):
            # e.g. "foo" or 2.5
            # exception message copied from numpy
            raise IndexError(
                r"only integers, slices (`:`), ellipsis (`...`), numpy.newaxis "
                r"(`None`) and integer or boolean arrays are valid indices"
            )

        else:
            if isinstance(key, SparseArray):
                # NOTE: If we guarantee that SparseDType(bool)
                # has only fill_value - true, false or nan
                # (see GH PR 44955)
                # we can apply mask very fast:
                if is_bool_dtype(key):
                    if isna(key.fill_value):
                        return self.take(key.sp_index.indices[key.sp_values])
                    if not key.fill_value:
                        return self.take(key.sp_index.indices)
                    n = len(self)
                    mask = np.full(n, True, dtype=np.bool_)
                    mask[key.sp_index.indices] = False
                    return self.take(np.arange(n)[mask])
                else:
                    key = np.asarray(key)

            key = check_array_indexer(self, key)

            if com.is_bool_indexer(key):
                # mypy doesn't know we have an array here
                key = cast(np.ndarray, key)
                return self.take(np.arange(len(key), dtype=np.int32)[key])
            elif hasattr(key, "__len__"):
                return self.take(key)
            else:
                raise ValueError(f"Cannot slice with '{key}'")

        return type(self)(data_slice, kind=self.kind)
