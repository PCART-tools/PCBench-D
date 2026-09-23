def _alignment_join(
    *idx_frames: tuple[int, LazyFrame],
    align_on: list[str],
    how: JoinStrategy = "full",
    descending: bool | Sequence[bool] = False,
) -> LazyFrame:
    """Create a single master frame with all rows aligned on the common key values."""
    # note: can stackoverflow if the join becomes too large, so we
    # collect eagerly when hitting a large enough number of frames
    post_align_collect = len(idx_frames) >= 250

    def join_func(
        idx_x: tuple[int, LazyFrame],
        idx_y: tuple[int, LazyFrame],
    ) -> tuple[int, LazyFrame]:
        (_, x), (y_idx, y) = idx_x, idx_y
        return y_idx, x.join(y, how=how, on=align_on, suffix=f":{y_idx}", coalesce=True)

    joined = reduce(join_func, idx_frames)[1].sort(by=align_on, descending=descending)
    if post_align_collect:
        joined = joined.collect(no_optimization=True).lazy()
    return joined
