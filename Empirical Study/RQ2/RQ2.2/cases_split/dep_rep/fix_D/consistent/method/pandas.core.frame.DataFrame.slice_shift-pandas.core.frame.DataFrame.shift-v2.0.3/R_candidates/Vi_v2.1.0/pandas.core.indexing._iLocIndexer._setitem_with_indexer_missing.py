    def _setitem_with_indexer_missing(self, indexer, value):
        """
        Insert new row(s) or column(s) into the Series or DataFrame.
        """
        from pandas import Series

        # reindex the axis to the new value
        # and set inplace
        if self.ndim == 1:
            index = self.obj.index
            new_index = index.insert(len(index), indexer)

            # we have a coerced indexer, e.g. a float
            # that matches in an int64 Index, so
            # we will not create a duplicate index, rather
            # index to that element
            # e.g. 0.0 -> 0
            # GH#12246
            if index.is_unique:
                # pass new_index[-1:] instead if [new_index[-1]]
                #  so that we retain dtype
                new_indexer = index.get_indexer(new_index[-1:])
                if (new_indexer != -1).any():
                    # We get only here with loc, so can hard code
                    return self._setitem_with_indexer(new_indexer, value, "loc")

            # this preserves dtype of the value and of the object
            if not is_scalar(value):
                new_dtype = None

            elif is_valid_na_for_dtype(value, self.obj.dtype):
                if not is_object_dtype(self.obj.dtype):
                    # Every NA value is suitable for object, no conversion needed
                    value = na_value_for_dtype(self.obj.dtype, compat=False)

                new_dtype = maybe_promote(self.obj.dtype, value)[0]

            elif isna(value):
                new_dtype = None
            elif not self.obj.empty and not is_object_dtype(self.obj.dtype):
                # We should not cast, if we have object dtype because we can
                # set timedeltas into object series
                curr_dtype = self.obj.dtype
                curr_dtype = getattr(curr_dtype, "numpy_dtype", curr_dtype)
                new_dtype = maybe_promote(curr_dtype, value)[0]
            else:
                new_dtype = None

            new_values = Series([value], dtype=new_dtype)._values

            if len(self.obj._values):
                # GH#22717 handle casting compatibility that np.concatenate
                #  does incorrectly
                new_values = concat_compat([self.obj._values, new_values])
            self.obj._mgr = self.obj._constructor(
                new_values, index=new_index, name=self.obj.name
            )._mgr
            self.obj._maybe_update_cacher(clear=True)

        elif self.ndim == 2:
            if not len(self.obj.columns):
                # no columns and scalar
                raise ValueError("cannot set a frame with no defined columns")

            has_dtype = hasattr(value, "dtype")
            if isinstance(value, ABCSeries):
                # append a Series
                value = value.reindex(index=self.obj.columns, copy=True)
                value.name = indexer
            elif isinstance(value, dict):
                value = Series(
                    value, index=self.obj.columns, name=indexer, dtype=object
                )
            else:
                # a list-list
                if is_list_like_indexer(value):
                    # must have conforming columns
                    if len(value) != len(self.obj.columns):
                        raise ValueError("cannot set a row with mismatched columns")

                value = Series(value, index=self.obj.columns, name=indexer)

            if not len(self.obj):
                # We will ignore the existing dtypes instead of using
                #  internals.concat logic
                df = value.to_frame().T

                idx = self.obj.index
                if isinstance(idx, MultiIndex):
                    name = idx.names
                else:
                    name = idx.name

                df.index = Index([indexer], name=name)
                if not has_dtype:
                    # i.e. if we already had a Series or ndarray, keep that
                    #  dtype.  But if we had a list or dict, then do inference
                    df = df.infer_objects(copy=False)
                self.obj._mgr = df._mgr
            else:
                self.obj._mgr = self.obj._append(value)._mgr
            self.obj._maybe_update_cacher(clear=True)
