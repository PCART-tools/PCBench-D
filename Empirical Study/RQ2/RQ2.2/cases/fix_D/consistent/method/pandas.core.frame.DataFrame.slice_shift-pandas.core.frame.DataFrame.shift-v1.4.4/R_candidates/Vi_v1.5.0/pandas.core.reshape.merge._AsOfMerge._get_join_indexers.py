    def _get_join_indexers(self) -> tuple[npt.NDArray[np.intp], npt.NDArray[np.intp]]:
        """return the join indexers"""

        def flip(xs) -> np.ndarray:
            """unlike np.transpose, this returns an array of tuples"""

            def injection(obj):
                if not is_extension_array_dtype(obj):
                    # ndarray
                    return obj
                obj = extract_array(obj)
                if isinstance(obj, NDArrayBackedExtensionArray):
                    # fastpath for e.g. dt64tz, categorical
                    return obj._ndarray
                # FIXME: returning obj._values_for_argsort() here doesn't
                #  break in any existing test cases, but i (@jbrockmendel)
                #  am pretty sure it should!
                #  e.g.
                #  arr = pd.array([0, pd.NA, 255], dtype="UInt8")
                #  will have values_for_argsort (before GH#45434)
                #  np.array([0, 255, 255], dtype=np.uint8)
                #  and the non-injectivity should make a difference somehow
                #  shouldn't it?
                return np.asarray(obj)

            xs = [injection(x) for x in xs]
            labels = list(string.ascii_lowercase[: len(xs)])
            dtypes = [x.dtype for x in xs]
            labeled_dtypes = list(zip(labels, dtypes))
            return np.array(list(zip(*xs)), labeled_dtypes)

        # values to compare
        left_values = (
            self.left.index._values if self.left_index else self.left_join_keys[-1]
        )
        right_values = (
            self.right.index._values if self.right_index else self.right_join_keys[-1]
        )
        tolerance = self.tolerance

        # we require sortedness and non-null values in the join keys
        if not Index(left_values).is_monotonic_increasing:
            side = "left"
            if isna(left_values).any():
                raise ValueError(f"Merge keys contain null values on {side} side")
            else:
                raise ValueError(f"{side} keys must be sorted")

        if not Index(right_values).is_monotonic_increasing:
            side = "right"
            if isna(right_values).any():
                raise ValueError(f"Merge keys contain null values on {side} side")
            else:
                raise ValueError(f"{side} keys must be sorted")

        # initial type conversion as needed
        if needs_i8_conversion(left_values):
            left_values = left_values.view("i8")
            right_values = right_values.view("i8")
            if tolerance is not None:
                tolerance = Timedelta(tolerance)
                tolerance = tolerance.value

        # a "by" parameter requires special handling
        if self.left_by is not None:
            # remove 'on' parameter from values if one existed
            if self.left_index and self.right_index:
                left_by_values = self.left_join_keys
                right_by_values = self.right_join_keys
            else:
                left_by_values = self.left_join_keys[0:-1]
                right_by_values = self.right_join_keys[0:-1]

            # get tuple representation of values if more than one
            if len(left_by_values) == 1:
                left_by_values = left_by_values[0]
                right_by_values = right_by_values[0]
            else:
                # We get here with non-ndarrays in test_merge_by_col_tz_aware
                #  and test_merge_groupby_multiple_column_with_categorical_column
                left_by_values = flip(left_by_values)
                right_by_values = flip(right_by_values)

            # upcast 'by' parameter because HashTable is limited
            by_type = _get_cython_type_upcast(left_by_values.dtype)
            by_type_caster = _type_casters[by_type]
            # error: Cannot call function of unknown type
            left_by_values = by_type_caster(left_by_values)  # type: ignore[operator]
            # error: Cannot call function of unknown type
            right_by_values = by_type_caster(right_by_values)  # type: ignore[operator]

            # choose appropriate function by type
            func = _asof_by_function(self.direction)
            return func(
                left_values,
                right_values,
                left_by_values,
                right_by_values,
                self.allow_exact_matches,
                tolerance,
            )
        else:
            # choose appropriate function by type
            func = _asof_by_function(self.direction)
            return func(
                left_values,
                right_values,
                None,
                None,
                self.allow_exact_matches,
                tolerance,
                False,
            )
