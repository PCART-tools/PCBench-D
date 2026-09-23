def rename_use_earliest_to_ambiguous(
    use_earliest: bool | None, ambiguous: Ambiguous | Expr
) -> Ambiguous | Expr:
    """Issue deprecation warning if deprecated `use_earliest` argument is used."""
    if isinstance(use_earliest, bool):
        ambiguous = USE_EARLIEST_TO_AMBIGUOUS[use_earliest]
        warnings.warn(
            "The argument 'use_earliest' in 'replace_time_zone' is deprecated. "
            f"Please replace `use_earliest={use_earliest}` with "
            f"`ambiguous='{ambiguous}'`. Note that this new argument can also "
            "accept expressions.",
            DeprecationWarning,
            stacklevel=find_stacklevel(),
        )
        return ambiguous
    return ambiguous
