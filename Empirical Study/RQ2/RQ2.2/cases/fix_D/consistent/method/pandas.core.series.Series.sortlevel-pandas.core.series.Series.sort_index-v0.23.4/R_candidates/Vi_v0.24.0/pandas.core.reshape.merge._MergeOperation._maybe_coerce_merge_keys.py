    def _maybe_coerce_merge_keys(self):
        # we have valid mergees but we may have to further
        # coerce these if they are originally incompatible types
        #
        # for example if these are categorical, but are not dtype_equal
        # or if we have object and integer dtypes

        for lk, rk, name in zip(self.left_join_keys,
                                self.right_join_keys,
                                self.join_names):
            if (len(lk) and not len(rk)) or (not len(lk) and len(rk)):
                continue

            lk_is_cat = is_categorical_dtype(lk)
            rk_is_cat = is_categorical_dtype(rk)
            lk_is_object = is_object_dtype(lk)
            rk_is_object = is_object_dtype(rk)

            # if either left or right is a categorical
            # then the must match exactly in categories & ordered
            if lk_is_cat and rk_is_cat:
                if lk.is_dtype_equal(rk):
                    continue

            elif lk_is_cat or rk_is_cat:
                pass

            elif is_dtype_equal(lk.dtype, rk.dtype):
                continue

            msg = ("You are trying to merge on {lk_dtype} and "
                   "{rk_dtype} columns. If you wish to proceed "
                   "you should use pd.concat".format(lk_dtype=lk.dtype,
                                                     rk_dtype=rk.dtype))

            # if we are numeric, then allow differing
            # kinds to proceed, eg. int64 and int8, int and float
            # further if we are object, but we infer to
            # the same, then proceed
            if is_numeric_dtype(lk) and is_numeric_dtype(rk):
                if lk.dtype.kind == rk.dtype.kind:
                    continue

                # check whether ints and floats
                elif is_integer_dtype(rk) and is_float_dtype(lk):
                    if not (lk == lk.astype(rk.dtype))[~np.isnan(lk)].all():
                        warnings.warn('You are merging on int and float '
                                      'columns where the float values '
                                      'are not equal to their int '
                                      'representation', UserWarning)
                    continue

                elif is_float_dtype(rk) and is_integer_dtype(lk):
                    if not (rk == rk.astype(lk.dtype))[~np.isnan(rk)].all():
                        warnings.warn('You are merging on int and float '
                                      'columns where the float values '
                                      'are not equal to their int '
                                      'representation', UserWarning)
                    continue

                # let's infer and see if we are ok
                elif (lib.infer_dtype(lk, skipna=False)
                      == lib.infer_dtype(rk, skipna=False)):
                    continue

            # Check if we are trying to merge on obviously
            # incompatible dtypes GH 9780, GH 15800

            # bool values are coerced to object
            elif ((lk_is_object and is_bool_dtype(rk)) or
                  (is_bool_dtype(lk) and rk_is_object)):
                pass

            # object values are allowed to be merged
            elif ((lk_is_object and is_numeric_dtype(rk)) or
                  (is_numeric_dtype(lk) and rk_is_object)):
                inferred_left = lib.infer_dtype(lk, skipna=False)
                inferred_right = lib.infer_dtype(rk, skipna=False)
                bool_types = ['integer', 'mixed-integer', 'boolean', 'empty']
                string_types = ['string', 'unicode', 'mixed', 'bytes', 'empty']

                # inferred bool
                if (inferred_left in bool_types and
                        inferred_right in bool_types):
                    pass

                # unless we are merging non-string-like with string-like
                elif ((inferred_left in string_types and
                       inferred_right not in string_types) or
                      (inferred_right in string_types and
                       inferred_left not in string_types)):
                    raise ValueError(msg)

            # datetimelikes must match exactly
            elif is_datetimelike(lk) and not is_datetimelike(rk):
                raise ValueError(msg)
            elif not is_datetimelike(lk) and is_datetimelike(rk):
                raise ValueError(msg)
            elif is_datetime64tz_dtype(lk) and not is_datetime64tz_dtype(rk):
                raise ValueError(msg)
            elif not is_datetime64tz_dtype(lk) and is_datetime64tz_dtype(rk):
                raise ValueError(msg)

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
                typ = lk.categories.dtype if lk_is_cat else object
                self.left = self.left.assign(
                    **{name: self.left[name].astype(typ)})
            if name in self.right.columns:
                typ = rk.categories.dtype if rk_is_cat else object
                self.right = self.right.assign(
                    **{name: self.right[name].astype(typ)})
