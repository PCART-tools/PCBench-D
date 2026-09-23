def apply_flat_fun(fun, io_tree, *py_args):
  in_tree_expected, out_tree = io_tree
  args, in_tree = tree_flatten((py_args, {}))
  if in_tree != in_tree_expected:
    raise TypeError(f"Expected {in_tree_expected}, got {in_tree}")
  ans = fun(*args)
  return tree_unflatten(out_tree, ans)
