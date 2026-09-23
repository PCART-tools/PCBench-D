    def _join_compat(
        self,
        other: DataFrame | Series | Iterable[DataFrame | Series],
        on: IndexLabel | None = None,
        how: MergeHow = "left",
        lsuffix: str = "",
        rsuffix: str = "",
        sort: bool = False,
        validate: str | None = None,
    ):
        from pandas.core.reshape.concat import concat
        from pandas.core.reshape.merge import merge

        if isinstance(other, Series):
            if other.name is None:
                raise ValueError("Other Series must have a name")
            other = DataFrame({other.name: other})

        if isinstance(other, DataFrame):
            if how == "cross":
                return merge(
                    self,
                    other,
                    how=how,
                    on=on,
                    suffixes=(lsuffix, rsuffix),
                    sort=sort,
                    validate=validate,
                )
            return merge(
                self,
                other,
                left_on=on,
                how=how,
                left_index=on is None,
                right_index=True,
                suffixes=(lsuffix, rsuffix),
                sort=sort,
                validate=validate,
            )
        else:
            if on is not None:
                raise ValueError(
                    "Joining multiple DataFrames only supported for joining on index"
                )

            if rsuffix or lsuffix:
                raise ValueError(
                    "Suffixes not supported when joining multiple DataFrames"
                )

            # Mypy thinks the RHS is a
            # "Union[DataFrame, Series, Iterable[Union[DataFrame, Series]]]" whereas
            # the LHS is an "Iterable[DataFrame]", but in reality both types are
            # "Iterable[Union[DataFrame, Series]]" due to the if statements
            frames = [cast("DataFrame | Series", self)] + list(other)

            can_concat = all(df.index.is_unique for df in frames)

            # join indexes only using concat
            if can_concat:
                if how == "left":
                    res = concat(
                        frames, axis=1, join="outer", verify_integrity=True, sort=sort
                    )
                    return res.reindex(self.index, copy=False)
                else:
                    return concat(
                        frames, axis=1, join=how, verify_integrity=True, sort=sort
                    )

            joined = frames[0]

            for frame in frames[1:]:
                joined = merge(
                    joined,
                    frame,
                    how=how,
                    left_index=True,
                    right_index=True,
                    validate=validate,
                )

            return joined
