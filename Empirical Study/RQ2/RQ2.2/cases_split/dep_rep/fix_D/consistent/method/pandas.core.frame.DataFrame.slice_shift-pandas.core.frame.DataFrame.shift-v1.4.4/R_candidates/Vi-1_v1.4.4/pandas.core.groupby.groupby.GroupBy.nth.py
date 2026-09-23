    @final
    @Substitution(name="groupby")
    @Substitution(see_also=_common_see_also)
    def nth(
        self,
        n: PositionalIndexer | tuple,
        dropna: Literal["any", "all", None] = None,
    ) -> NDFrameT:
        """
        Take the nth row from each group if n is an int, otherwise a subset of rows.

        Can be either a call or an index. dropna is not available with index notation.
        Index notation accepts a comma separated list of integers and slices.

        If dropna, will take the nth non-null row, dropna is either
        'all' or 'any'; this is equivalent to calling dropna(how=dropna)
        before the groupby.

        Parameters
        ----------
        n : int, slice or list of ints and slices
            A single nth value for the row or a list of nth values or slices.

            .. versionchanged:: 1.4.0
                Added slice and lists containing slices.
                Added index notation.

        dropna : {'any', 'all', None}, default None
            Apply the specified dropna operation before counting which row is
            the nth row. Only supported if n is an int.

        Returns
        -------
        Series or DataFrame
            N-th value within each group.
        %(see_also)s
        Examples
        --------

        >>> df = pd.DataFrame({'A': [1, 1, 2, 1, 2],
        ...                    'B': [np.nan, 2, 3, 4, 5]}, columns=['A', 'B'])
        >>> g = df.groupby('A')
        >>> g.nth(0)
             B
        A
        1  NaN
        2  3.0
        >>> g.nth(1)
             B
        A
        1  2.0
        2  5.0
        >>> g.nth(-1)
             B
        A
        1  4.0
        2  5.0
        >>> g.nth([0, 1])
             B
        A
        1  NaN
        1  2.0
        2  3.0
        2  5.0
        >>> g.nth(slice(None, -1))
             B
        A
        1  NaN
        1  2.0
        2  3.0

        Index notation may also be used

        >>> g.nth[0, 1]
             B
        A
        1  NaN
        1  2.0
        2  3.0
        2  5.0
        >>> g.nth[:-1]
             B
        A
        1  NaN
        1  2.0
        2  3.0

        Specifying `dropna` allows count ignoring ``NaN``

        >>> g.nth(0, dropna='any')
             B
        A
        1  2.0
        2  3.0

        NaNs denote group exhausted when using dropna

        >>> g.nth(3, dropna='any')
            B
        A
        1 NaN
        2 NaN

        Specifying `as_index=False` in `groupby` keeps the original index.

        >>> df.groupby('A', as_index=False).nth(1)
           A    B
        1  1  2.0
        4  2  5.0
        """
        if not dropna:
            with self._group_selection_context():
                mask = self._make_mask_from_positional_indexer(n)

                ids, _, _ = self.grouper.group_info

                # Drop NA values in grouping
                mask = mask & (ids != -1)

                out = self._mask_selected_obj(mask)
                if not self.as_index:
                    return out

                result_index = self.grouper.result_index
                if self.axis == 0:
                    out.index = result_index[ids[mask]]
                    if not self.observed and isinstance(result_index, CategoricalIndex):
                        out = out.reindex(result_index)

                    out = self._reindex_output(out)
                else:
                    out.columns = result_index[ids[mask]]

                return out.sort_index(axis=self.axis) if self.sort else out

        # dropna is truthy
        if not is_integer(n):
            raise ValueError("dropna option only supported for an integer argument")

        if dropna not in ["any", "all"]:
            # Note: when agg-ing picker doesn't raise this, just returns NaN
            raise ValueError(
                "For a DataFrame or Series groupby.nth, dropna must be "
                "either None, 'any' or 'all', "
                f"(was passed {dropna})."
            )

        # old behaviour, but with all and any support for DataFrames.
        # modified in GH 7559 to have better perf
        n = cast(int, n)
        max_len = n if n >= 0 else -1 - n
        dropped = self.obj.dropna(how=dropna, axis=self.axis)

        # get a new grouper for our dropped obj
        if self.keys is None and self.level is None:

            # we don't have the grouper info available
            # (e.g. we have selected out
            # a column that is not in the current object)
            axis = self.grouper.axis
            grouper = axis[axis.isin(dropped.index)]

        else:

            # create a grouper with the original parameters, but on dropped
            # object
            from pandas.core.groupby.grouper import get_grouper

            grouper, _, _ = get_grouper(
                dropped,
                key=self.keys,
                axis=self.axis,
                level=self.level,
                sort=self.sort,
                mutated=self.mutated,
            )

        grb = dropped.groupby(
            grouper, as_index=self.as_index, sort=self.sort, axis=self.axis
        )
        sizes, result = grb.size(), grb.nth(n)
        mask = (sizes < max_len)._values

        # set the results which don't meet the criteria
        if len(result) and mask.any():
            result.loc[mask] = np.nan

        # reset/reindex to the original groups
        if len(self.obj) == len(dropped) or len(result) == len(
            self.grouper.result_index
        ):
            result.index = self.grouper.result_index
        else:
            result = result.reindex(self.grouper.result_index)

        return result
