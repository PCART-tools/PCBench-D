    def __setitem__(self, key, value) -> None:
        check_deprecated_indexers(key)
        key = com.apply_if_callable(key, self)
        cacher_needs_updating = self._check_is_chained_assignment_possible()

        if key is Ellipsis:
            key = slice(None)

        if isinstance(key, slice):
            indexer = self.index._convert_slice_indexer(key, kind="getitem")
            return self._set_values(indexer, value)

        try:
            self._set_with_engine(key, value)
        except (KeyError, ValueError):
            if is_integer(key) and self.index.inferred_type != "integer":
                # positional setter
                if not self.index._should_fallback_to_positional:
                    # GH#33469
                    warnings.warn(
                        "Treating integers as positional in Series.__setitem__ "
                        "with a Float64Index is deprecated. In a future version, "
                        "`series[an_int] = val` will insert a new key into the "
                        "Series. Use `series.iloc[an_int] = val` to treat the "
                        "key as positional.",
                        FutureWarning,
                        stacklevel=find_stack_level(),
                    )
                # this is equivalent to self._values[key] = value
                self._mgr.setitem_inplace(key, value)
            else:
                # GH#12862 adding a new key to the Series
                self.loc[key] = value

        except (InvalidIndexError, TypeError) as err:
            if isinstance(key, tuple) and not isinstance(self.index, MultiIndex):
                # cases with MultiIndex don't get here bc they raise KeyError
                raise KeyError(
                    "key of type tuple not found and not a MultiIndex"
                ) from err

            if com.is_bool_indexer(key):
                key = check_bool_indexer(self.index, key)
                key = np.asarray(key, dtype=bool)

                if (
                    is_list_like(value)
                    and len(value) != len(self)
                    and not isinstance(value, Series)
                    and not is_object_dtype(self.dtype)
                ):
                    # Series will be reindexed to have matching length inside
                    #  _where call below
                    # GH#44265
                    indexer = key.nonzero()[0]
                    self._set_values(indexer, value)
                    return

                # otherwise with listlike other we interpret series[mask] = other
                #  as series[mask] = other[mask]
                try:
                    self._where(~key, value, inplace=True)
                except InvalidIndexError:
                    # test_where_dups
                    self.iloc[key] = value
                return

            else:
                self._set_with(key, value)

        if cacher_needs_updating:
            self._maybe_update_cacher(inplace=True)
