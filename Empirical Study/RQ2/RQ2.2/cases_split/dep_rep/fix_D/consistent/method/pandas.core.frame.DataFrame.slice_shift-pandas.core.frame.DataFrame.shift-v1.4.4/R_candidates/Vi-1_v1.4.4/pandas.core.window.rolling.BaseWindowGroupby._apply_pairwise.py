    def _apply_pairwise(
        self,
        target: DataFrame | Series,
        other: DataFrame | Series | None,
        pairwise: bool | None,
        func: Callable[[DataFrame | Series, DataFrame | Series], DataFrame | Series],
    ) -> DataFrame | Series:
        """
        Apply the given pairwise function given 2 pandas objects (DataFrame/Series)
        """
        # Manually drop the grouping column first
        target = target.drop(columns=self._grouper.names, errors="ignore")
        target = self._create_data(target)
        result = super()._apply_pairwise(target, other, pairwise, func)
        # 1) Determine the levels + codes of the groupby levels
        if other is not None and not all(
            len(group) == len(other) for group in self._grouper.indices.values()
        ):
            # GH 42915
            # len(other) != len(any group), so must reindex (expand) the result
            # from flex_binary_moment to a "transform"-like result
            # per groupby combination
            old_result_len = len(result)
            result = concat(
                [
                    result.take(gb_indices).reindex(result.index)
                    for gb_indices in self._grouper.indices.values()
                ]
            )

            gb_pairs = (
                com.maybe_make_list(pair) for pair in self._grouper.indices.keys()
            )
            groupby_codes = []
            groupby_levels = []
            # e.g. [[1, 2], [4, 5]] as [[1, 4], [2, 5]]
            for gb_level_pair in map(list, zip(*gb_pairs)):
                labels = np.repeat(np.array(gb_level_pair), old_result_len)
                codes, levels = factorize(labels)
                groupby_codes.append(codes)
                groupby_levels.append(levels)
        else:
            # pairwise=True or len(other) == len(each group), so repeat
            # the groupby labels by the number of columns in the original object
            groupby_codes = self._grouper.codes
            # error: Incompatible types in assignment (expression has type
            # "List[Index]", variable has type "List[Union[ndarray, Index]]")
            groupby_levels = self._grouper.levels  # type: ignore[assignment]

            group_indices = self._grouper.indices.values()
            if group_indices:
                indexer = np.concatenate(list(group_indices))
            else:
                indexer = np.array([], dtype=np.intp)

            if target.ndim == 1:
                repeat_by = 1
            else:
                repeat_by = len(target.columns)
            groupby_codes = [
                np.repeat(c.take(indexer), repeat_by) for c in groupby_codes
            ]
        # 2) Determine the levels + codes of the result from super()._apply_pairwise
        if isinstance(result.index, MultiIndex):
            result_codes = list(result.index.codes)
            result_levels = list(result.index.levels)
            result_names = list(result.index.names)
        else:
            idx_codes, idx_levels = factorize(result.index)
            result_codes = [idx_codes]
            result_levels = [idx_levels]
            result_names = [result.index.name]

        # 3) Create the resulting index by combining 1) + 2)
        result_codes = groupby_codes + result_codes
        result_levels = groupby_levels + result_levels
        result_names = self._grouper.names + result_names

        result_index = MultiIndex(
            result_levels, result_codes, names=result_names, verify_integrity=False
        )
        result.index = result_index
        return result
