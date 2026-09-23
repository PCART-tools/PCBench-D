    def _setitem_with_indexer_split_path(self, indexer, value, name: str):
        """
        Setitem column-wise.
        """
        # Above we only set take_split_path to True for 2D cases
        assert self.ndim == 2

        if not isinstance(indexer, tuple):
            indexer = _tuplify(self.ndim, indexer)
        if len(indexer) > self.ndim:
            raise IndexError("too many indices for array")
        if isinstance(indexer[0], np.ndarray) and indexer[0].ndim > 2:
            raise ValueError(r"Cannot set values with ndim > 2")

        if (isinstance(value, ABCSeries) and name != "iloc") or isinstance(value, dict):
            from pandas import Series

            value = self._align_series(indexer, Series(value))

        # Ensure we have something we can iterate over
        info_axis = indexer[1]
        ilocs = self._ensure_iterable_column_indexer(info_axis)

        pi = indexer[0]
        lplane_indexer = length_of_indexer(pi, self.obj.index)
        # lplane_indexer gives the expected length of obj[indexer[0]]

        # we need an iterable, with a ndim of at least 1
        # eg. don't pass through np.array(0)
        if is_list_like_indexer(value) and getattr(value, "ndim", 1) > 0:
            if isinstance(value, ABCDataFrame):
                self._setitem_with_indexer_frame_value(indexer, value, name)

            elif np.ndim(value) == 2:
                # TODO: avoid np.ndim call in case it isn't an ndarray, since
                #  that will construct an ndarray, which will be wasteful
                self._setitem_with_indexer_2d_value(indexer, value)

            elif len(ilocs) == 1 and lplane_indexer == len(value) and not is_scalar(pi):
                # We are setting multiple rows in a single column.
                self._setitem_single_column(ilocs[0], value, pi)

            elif len(ilocs) == 1 and 0 != lplane_indexer != len(value):
                # We are trying to set N values into M entries of a single
                #  column, which is invalid for N != M
                # Exclude zero-len for e.g. boolean masking that is all-false

                if len(value) == 1 and not is_integer(info_axis):
                    # This is a case like df.iloc[:3, [1]] = [0]
                    #  where we treat as df.iloc[:3, 1] = 0
                    return self._setitem_with_indexer((pi, info_axis[0]), value[0])

                raise ValueError(
                    "Must have equal len keys and value "
                    "when setting with an iterable"
                )

            elif lplane_indexer == 0 and len(value) == len(self.obj.index):
                # We get here in one case via .loc with a all-False mask
                pass

            elif self._is_scalar_access(indexer) and is_object_dtype(
                self.obj.dtypes._values[ilocs[0]]
            ):
                # We are setting nested data, only possible for object dtype data
                self._setitem_single_column(indexer[1], value, pi)

            elif len(ilocs) == len(value):
                # We are setting multiple columns in a single row.
                for loc, v in zip(ilocs, value):
                    self._setitem_single_column(loc, v, pi)

            elif len(ilocs) == 1 and com.is_null_slice(pi) and len(self.obj) == 0:
                # This is a setitem-with-expansion, see
                #  test_loc_setitem_empty_append_expands_rows_mixed_dtype
                # e.g. df = DataFrame(columns=["x", "y"])
                #  df["x"] = df["x"].astype(np.int64)
                #  df.loc[:, "x"] = [1, 2, 3]
                self._setitem_single_column(ilocs[0], value, pi)

            else:
                raise ValueError(
                    "Must have equal len keys and value "
                    "when setting with an iterable"
                )

        else:
            # scalar value
            for loc in ilocs:
                self._setitem_single_column(loc, value, pi)
