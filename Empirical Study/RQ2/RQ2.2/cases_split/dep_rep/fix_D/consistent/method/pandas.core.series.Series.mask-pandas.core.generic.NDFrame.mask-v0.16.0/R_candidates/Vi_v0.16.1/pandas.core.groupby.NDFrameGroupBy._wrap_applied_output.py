    def _wrap_applied_output(self, keys, values, not_indexed_same=False):
        from pandas.core.index import _all_indexes_same

        if len(keys) == 0:
            # XXX
            return DataFrame({})

        key_names = self.grouper.names

        if isinstance(values[0], DataFrame):
            return self._concat_objects(keys, values,
                                        not_indexed_same=not_indexed_same)
        elif self.grouper.groupings is not None:
            if len(self.grouper.groupings) > 1:
                key_index = MultiIndex.from_tuples(keys, names=key_names)

            else:
                ping = self.grouper.groupings[0]
                if len(keys) == ping.ngroups:
                    key_index = ping.group_index
                    key_index.name = key_names[0]

                    key_lookup = Index(keys)
                    indexer = key_lookup.get_indexer(key_index)

                    # reorder the values
                    values = [values[i] for i in indexer]
                else:

                    key_index = Index(keys, name=key_names[0])

                # don't use the key indexer
                if not self.as_index:
                    key_index = None

            # make Nones an empty object
            if com._count_not_none(*values) != len(values):
                try:
                    v = next(v for v in values if v is not None)
                except StopIteration:
                    # If all values are None, then this will throw an error.
                    # We'd prefer it return an empty dataframe.
                    return DataFrame()
                if v is None:
                    return DataFrame()
                elif isinstance(v, NDFrame):
                    values = [
                        x if x is not None else
                        v._constructor(**v._construct_axes_dict())
                        for x in values
                        ]

            v = values[0]

            if isinstance(v, (np.ndarray, Index, Series)):
                if isinstance(v, Series):
                    applied_index = self._selected_obj._get_axis(self.axis)
                    all_indexed_same = _all_indexes_same([
                        x.index for x in values
                    ])
                    singular_series = (len(values) == 1 and
                                       applied_index.nlevels == 1)

                    # GH3596
                    # provide a reduction (Frame -> Series) if groups are
                    # unique
                    if self.squeeze:

                        # assign the name to this series
                        if singular_series:
                            values[0].name = keys[0]

                            # GH2893
                            # we have series in the values array, we want to
                            # produce a series:
                            # if any of the sub-series are not indexed the same
                            # OR we don't have a multi-index and we have only a
                            # single values
                            return self._concat_objects(
                                keys, values, not_indexed_same=not_indexed_same
                            )

                        # still a series
                        # path added as of GH 5545
                        elif all_indexed_same:
                            from pandas.tools.merge import concat
                            return concat(values)

                    if not all_indexed_same:
                        # GH 8467
                        return self._concat_objects(
                            keys, values, not_indexed_same=True,
                        )

                try:
                    if self.axis == 0:
                        # GH6124 if the list of Series have a consistent name,
                        # then propagate that name to the result.
                        index = v.index.copy()
                        if index.name is None:
                            # Only propagate the series name to the result
                            # if all series have a consistent name.  If the
                            # series do not have a consistent name, do
                            # nothing.
                            names = set(v.name for v in values)
                            if len(names) == 1:
                                index.name = list(names)[0]

                        # normally use vstack as its faster than concat
                        # and if we have mi-columns
                        if isinstance(v.index, MultiIndex) or key_index is None:
                            stacked_values = np.vstack(map(np.asarray, values))
                            result = DataFrame(stacked_values, index=key_index,
                                               columns=index)
                        else:
                            # GH5788 instead of stacking; concat gets the dtypes correct
                            from pandas.tools.merge import concat
                            result = concat(values, keys=key_index,
                                            names=key_index.names,
                                            axis=self.axis).unstack()
                            result.columns = index
                    else:
                        stacked_values = np.vstack(map(np.asarray, values))
                        result = DataFrame(stacked_values.T, index=v.index,
                                           columns=key_index)

                except (ValueError, AttributeError):
                    # GH1738: values is list of arrays of unequal lengths fall
                    # through to the outer else caluse
                    return Series(values, index=key_index)

                # if we have date/time like in the original, then coerce dates
                # as we are stacking can easily have object dtypes here
                if (self._selected_obj.ndim == 2
                       and self._selected_obj.dtypes.isin(_DATELIKE_DTYPES).any()):
                    cd = 'coerce'
                else:
                    cd = True
                return result.convert_objects(convert_dates=cd)

            else:
                # only coerce dates if we find at least 1 datetime
                cd = 'coerce' if any([ isinstance(v,Timestamp) for v in values ]) else False
                return Series(values, index=key_index).convert_objects(convert_dates=cd)

        else:
            # Handle cases like BinGrouper
            return self._concat_objects(keys, values,
                                        not_indexed_same=not_indexed_same)
