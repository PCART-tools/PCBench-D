def _get_arg_names(fun, in_tree, args_flat):
  sig = _try_infer_args(fun, in_tree)
  args_aug = generate_key_paths(tree_unflatten(in_tree, args_flat))

  arg_names = []
  for arg_key, val in args_aug:
    ak, *rem_keys = arg_key
    if sig is not None:
      loc = ''.join(str(k) for k in rem_keys)
      arg_name = f'{list(sig.arguments.keys())[ak.idx]}{loc}'
    else:
      arg_name = ''
    arg_names.append(arg_name)
  return arg_names
