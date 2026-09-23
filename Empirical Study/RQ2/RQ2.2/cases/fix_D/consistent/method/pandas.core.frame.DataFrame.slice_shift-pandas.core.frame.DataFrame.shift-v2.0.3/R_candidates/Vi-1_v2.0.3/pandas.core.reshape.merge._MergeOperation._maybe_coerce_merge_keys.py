    def _maybe_coerce_merge_keys(self) -> None:
        # we have valid merges but we may have to further
        # coerce these if they are originally incompatible types
        #
        # for example if these are categorical, but are not dtype_equal
        # or if we have object and integer dtypes

        for lk, rk, name in zip(
            self.left_join_keys, self.right_join_keys, self.join_names
        ):
            if (len(lk) and not len(rk)) or (not len(lk) and len(rk)):
                continue

            lk = extract_array(lk, extract_numpy=True)
            rk = extract_array(rk, extract_numpy=True)

            lk_is_cat = is_categorical_dtype(lk.dtype)
            rk_is_cat = is_categorical_dtype(rk.dtype)
            lk_is_object = is_object_dtype(lk.dtype)
            rk_is_object = is_object_dtype(rk.dtype)

            # if either left or right is a categorical
            # then the must match exactly in categories & ordered
            if lk_is_cat and rk_is_cat:
                lk = cast(Categorical, lk)
                rk = cast(Categorical, rk)
                if lk._categories_match_up_to_permutation(rk):
                    continue

            elif lk_is_cat or rk_is_cat:
                pass

            elif is_dtype_equal(lk.dtype, rk.dtype):
                continue

            msg = (
                f"You are trying to merge on {lk.dtype} and "
                f"{rk.dtype} columns. If you wish to proceed you should use pd.concat"
            )

            # if we are numeric, then allow differing
            # kinds to proceed, eg. int64 and int8, int and float
            # further if we are object, but we infer to
            # the same, then proceed
            if is_numeric_dtype(lk.dtype) and is_numeric_dtype(rk.dtype):
                if lk.dtype.kind == rk.dtype.kind:
                    continue

                # check whether ints and floats
                if is_integer_dtype(rk.dtype) and is_float_dtype(lk.dtype):
                    # GH 47391 numpy > 1.24 will raise a RuntimeError for nan -> int
                    with np.errstate(invalid="ignore"):
                        # error: Argument 1 to "astype" of "ndarray" has incompatible
                        # type "Union[ExtensionDtype, Any, dtype[Any]]"; expected
                        # "Union[dtype[Any], Type[Any], _SupportsDType[dtype[Any]]]"
                        casted = lk.astype(rk.dtype)  # type: ignore[arg-type]

                        mask = ~np.isnan(lk)
                        match = lk == casted
                        if not match[mask].all():
                            warnings.warn(
                                "You are merging on int and float "
                                "columns where the float values "
                                "are not equal to their int representation.",
                                UserWarning,
                                stacklevel=find_stack_level(),
                            )
                    continue

                if is_float_dtype(rk.dtype) and is_integer_dtype(lk.dtype):
                    # GH 47391 numpy > 1.24 will raise a RuntimeError for nan -> int
                    with np.errstate(invalid="ignore"):
                        # error: Argument 1 to "astype" of "ndarray" has incompatible
                        # type "Union[ExtensionDtype, Any, dtype[Any]]"; expected
                        # "Union[dtype[Any], Type[Any], _SupportsDType[dtype[Any]]]"
                        casted = rk.astype(lk.dtype)  # type: ignore[arg-type]

                        mask = ~np.isnan(rk)
                        match = rk == casted
                        if not match[mask].all():
                            warnings.warn(
                                "You are merging on int and float "
                                "columns where the float values "
                                "are not equal to their int representation.",
                                UserWarning,
                                stacklevel=find_stack_level(),
                            )
                    continue

                # let's infer and see if we are ok
                if lib.infer_dtype(lk, skipna=False) == lib.infer_dtype(
                    rk, skipna=False
                ):
                    continue

            # Check if we are trying to merge on obviously
            # incompatible dtypes GH 9780, GH 15800

            # bool values are coerced to object
            elif (lk_is_object and is_bool_dtype(rk.dtype)) or (
                is_bool_dtype(lk.dtype) and rk_is_object
            ):
                pass

            # object values are allowed to be merged
            elif (lk_is_object and is_numeric_dtype(rk.dtype)) or (
                is_numeric_dtype(lk.dtype) and rk_is_object
            ):
                inferred_left = lib.infer_dtype(lk, skipna=False)
                inferred_right = lib.infer_dtype(rk, skipna=False)
                bool_types = ["integer", "mixed-integer", "boolean", "empty"]
                string_types = ["string", "unicode", "mixed", "bytes", "empty"]

                # inferred bool
                if inferred_left in bool_types and inferred_right in bool_types:
                    pass

                # unless we are merging non-string-like with string-like
                elif (
                    inferred_left in string_types and inferred_right not in string_types
                ) or (
                    inferred_right in string_types and inferred_left not in string_types
                ):
                    raise ValueError(msg)

            # datetimelikes must match exactly
            elif needs_i8_conversion(lk.dtype) and not needs_i8_conversion(rk.dtype):
                raise ValueError(msg)
            elif not needs_i8_conversion(lk.dtype) and needs_i8_conversion(rk.dtype):
                raise ValueError(msg)
            elif isinstance(lk.dtype, DatetimeTZDtype) and not isinstance(
                rk.dtype, DatetimeTZDtype
            ):
                raise ValueError(msg)
            elif not isinstance(lk.dtype, DatetimeTZDtype) and isinstance(
                rk.dtype, DatetimeTZDtype
            ):
                raise ValueError(msg)
            elif (
                isinstance(lk.dtype, DatetimeTZDtype)
                and isinstance(rk.dtype, DatetimeTZDtype)
            ) or (lk.dtype.kind == "M" and rk.dtype.kind == "M"):
                # allows datetime with different resolutions
                continue

            elif lk_is_object and rk_is_object:
                continue

            # Houston, we have a problem!
            # let's coerce to object if the dtypes aren't
            # categorical, otherwise coerce to the category
            # dtype. If we coerced categories to object,
            # then we would lose type information on some
            # columns, and end up trying to merge
            # incompatible dtypes. See GH 16900.
            if name in self.left.columns:
                typ = cast(Categorical, lk).categories.dtype if lk_is_cat else object
                self.left = self.left.copy()
                self.left[name] = self.left[name].astype(typ)
            if name in self.right.columns:
                typ = cast(Categorical, rk).categories.dtype if rk_is_cat else object
                self.right = self.right.copy()
                self.right[name] = self.right[name].astype(typ)
