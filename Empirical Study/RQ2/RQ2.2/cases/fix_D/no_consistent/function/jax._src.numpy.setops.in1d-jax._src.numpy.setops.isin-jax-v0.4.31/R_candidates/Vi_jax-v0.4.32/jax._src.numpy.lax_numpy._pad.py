@partial(jit, static_argnums=(1, 2, 4, 5, 6))
def _pad(array: ArrayLike, pad_width: PadValueLike[int], mode: str,
         constant_values: ArrayLike, stat_length: PadValueLike[int],
         end_values: PadValueLike[ArrayLike], reflect_type: str):
  array = asarray(array)
  nd = ndim(array)

  if nd == 0:
    return array

  stat_funcs: dict[str, PadStatFunc] = {
      "maximum": reductions.amax,
      "minimum": reductions.amin,
      "mean": reductions.mean,
      "median": reductions.median
  }

  pad_width = _broadcast_to_pairs(pad_width, nd, "pad_width")
  pad_width_arr = np.array(pad_width)
  if pad_width_arr.shape != (nd, 2):
    raise ValueError(f"Expected pad_width to have shape {(nd, 2)}; got {pad_width_arr.shape}.")

  if np.any(pad_width_arr < 0):
    raise ValueError("index can't contain negative values")

  if mode == "constant":
    return _pad_constant(array, pad_width, asarray(constant_values))

  elif mode == "wrap":
    return _pad_wrap(array, pad_width)

  elif mode in ("symmetric", "reflect"):
    return _pad_symmetric_or_reflect(array, pad_width, str(mode), reflect_type)

  elif mode == "edge":
    return _pad_edge(array, pad_width)

  elif mode == "linear_ramp":
    end_values = _broadcast_to_pairs(end_values, nd, "end_values")
    return _pad_linear_ramp(array, pad_width, end_values)

  elif mode in stat_funcs:
    if stat_length is not None:
      stat_length = _broadcast_to_pairs(stat_length, nd, "stat_length")
    return _pad_stats(array, pad_width, stat_length, stat_funcs[str(mode)])

  elif mode == "empty":
    return _pad_empty(array, pad_width)

  else:
    assert False, ("Should not be reached since pad already handled unsupported and"
                   "not implemented modes")
