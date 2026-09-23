def get_input_metadata(
    global_in_avals: Sequence[ShapedArray],
    in_shardings: Sequence[sharding_internal.XLACompatibleSharding], in_is_global: Sequence[bool]
) -> Tuple[Sequence[sharding_internal.XLACompatibleSharding], Sequence[Tuple[Optional[Index], ...]],
           Sequence[ShapedArray]]:
  avals, shardings = _get_normalized_avals_and_shardings(
      global_in_avals, in_shardings, in_is_global)
  return shardings, _get_input_indices(avals, shardings), avals
