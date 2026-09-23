def promote_dtypes(*args: ArrayLike) -> list[Array]:
  """Convenience function to apply Numpy argument dtype promotion."""
  # TODO(dougalm,mattjj): This is a performance bottleneck. Consider memoizing.
  if len(args) < 2:
    return [lax.asarray(arg) for arg in args]
  else:
    to_dtype, weak_type = dtypes._lattice_result_type(*args)
    to_dtype = dtypes.canonicalize_dtype(to_dtype, allow_extended_dtype=True)  # type: ignore[assignment]
    return [lax._convert_element_type(x, to_dtype, weak_type) for x in args]
