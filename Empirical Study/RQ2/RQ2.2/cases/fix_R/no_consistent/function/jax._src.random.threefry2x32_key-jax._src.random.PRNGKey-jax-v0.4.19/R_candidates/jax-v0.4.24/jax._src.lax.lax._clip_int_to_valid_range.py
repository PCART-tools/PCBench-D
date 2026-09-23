def _clip_int_to_valid_range(val: int, dtype) -> int:
  info = np.iinfo(dtype)
  return builtins.max(info.min, builtins.min(int(val), info.max))
