@lu.transformation_with_aux
def flatten_fun_nokwargs(in_tree, *args_flat):
  py_args = tree_unflatten(in_tree, args_flat)
  ans = yield py_args, {}
  yield tree_flatten(ans)
