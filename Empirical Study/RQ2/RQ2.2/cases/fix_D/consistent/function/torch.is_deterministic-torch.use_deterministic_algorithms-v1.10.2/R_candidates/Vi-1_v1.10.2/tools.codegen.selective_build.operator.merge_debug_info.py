def merge_debug_info(
        lhs: Optional[Tuple[str, ...]],
        rhs: Optional[Tuple[str, ...]],
) -> Optional[Tuple[str, ...]]:
    # Ensure that when merging, each entry shows up just once.
    if lhs is None and rhs is None:
        return None

    return tuple(set((lhs or ()) + (rhs or ())))
