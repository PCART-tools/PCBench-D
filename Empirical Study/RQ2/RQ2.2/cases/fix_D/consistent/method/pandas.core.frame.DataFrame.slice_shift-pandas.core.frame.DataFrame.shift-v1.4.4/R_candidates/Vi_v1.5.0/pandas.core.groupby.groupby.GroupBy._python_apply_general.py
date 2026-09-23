    @final
    def _python_apply_general(
        self,
        f: Callable,
        data: DataFrame | Series,
        not_indexed_same: bool | None = None,
        is_transform: bool = False,
        is_agg: bool = False,
    ) -> NDFrameT:
        """
        Apply function f in python space

        Parameters
        ----------
        f : callable
            Function to apply
        data : Series or DataFrame
            Data to apply f to
        not_indexed_same: bool, optional
            When specified, overrides the value of not_indexed_same. Apply behaves
            differently when the result index is equal to the input index, but
            this can be coincidental leading to value-dependent behavior.
        is_transform : bool, default False
            Indicator for whether the function is actually a transform
            and should not have group keys prepended. This is used
            in _make_wrapper which generates both transforms (e.g. diff)
            and non-transforms (e.g. corr)
        is_agg : bool, default False
            Indicator for whether the function is an aggregation. When the
            result is empty, we don't want to warn for this case.
            See _GroupBy._python_agg_general.

        Returns
        -------
        Series or DataFrame
            data after applying f
        """
        values, mutated = self.grouper.apply(f, data, self.axis)
        if not_indexed_same is None:
            not_indexed_same = mutated or self.mutated
        override_group_keys = False

        is_empty_agg = is_agg and len(values) == 0
        if (not not_indexed_same and self.group_keys is lib.no_default) and not (
            is_transform or is_empty_agg
        ):
            # We've detected value-dependent behavior: the result's index depends on
            # whether the user's function `f` returned the same index or not.
            msg = (
                "Not prepending group keys to the result index of "
                "transform-like apply. In the future, the group keys "
                "will be included in the index, regardless of whether "
                "the applied function returns a like-indexed object.\n"
                "To preserve the previous behavior, use\n\n\t"
                ">>> .groupby(..., group_keys=False)\n\n"
                "To adopt the future behavior and silence this warning, use "
                "\n\n\t>>> .groupby(..., group_keys=True)"
            )
            warnings.warn(
                msg, FutureWarning, stacklevel=find_stack_level(inspect.currentframe())
            )
            # We want to behave as if `self.group_keys=False` when reconstructing
            # the object. However, we don't want to mutate the stateful GroupBy
            # object, so we just override it.
            # When this deprecation is enforced then override_group_keys
            # may be removed.
            override_group_keys = True

        return self._wrap_applied_output(
            data,
            values,
            not_indexed_same,
            override_group_keys=is_transform or override_group_keys,
        )
