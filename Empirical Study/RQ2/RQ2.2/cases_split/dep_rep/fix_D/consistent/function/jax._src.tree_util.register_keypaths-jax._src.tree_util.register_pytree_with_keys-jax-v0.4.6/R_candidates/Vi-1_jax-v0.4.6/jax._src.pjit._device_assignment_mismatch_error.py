def _device_assignment_mismatch_error(fun, fails, in_tree, args_flat, api_name):
  sig = _try_infer_args(fun, in_tree)
  args = tree_unflatten(in_tree, args_flat)
  args_aug = _generate_key_paths(args)

  arg_list = []
  for arg_key, val in args_aug:
    ak, *rem_keys = arg_key
    if sig is not None:
      loc = ''.join(str(k) for k in rem_keys)
      arg_name = f'{list(sig.arguments.keys())[ak.idx]}{loc}'
    else:
      arg_name = ''
    da = val.sharding._device_assignment if hasattr(val, 'sharding') else None
    arg_list.append((arg_name, da, shaped_abstractify(val)))

  fun_name = getattr(fun, '__qualname__', getattr(fun, '__name__', str(fun)))
  mismatched_args_msg = _find_arg_mismatch(arg_list, fails, fun_name)

  if len(mismatched_args_msg) == 2:
    first, second = mismatched_args_msg  # pylint: disable=unbalanced-tuple-unpacking
    extra_msg = f" Got {first} and {second}"
  elif len(mismatched_args_msg) == 1:
    first, second  = fails
    # Choose the failure left which is not already covered by ARG_SHARDING.
    left = second if first.m_type == pxla.MismatchType.ARG_SHARDING else first
    extra_msg = f" Got {mismatched_args_msg[0]} and{left._str(api_name)}"
  else:
    first, second = fails
    extra_msg = f" Got{first._str(api_name)} and{second._str(api_name)}"
  msg = (f"Received incompatible devices for {api_name}ted computation.{extra_msg}")
  return msg
