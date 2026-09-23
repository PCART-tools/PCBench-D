@lu.transformation_with_aux
def flatten_fun_for_vmap(in_tree, *args_flat):
  py_args, py_kwargs = tree_unflatten(in_tree, args_flat)
  ans = yield py_args, py_kwargs
  yield tree_flatten(ans, is_leaf=is_vmappable)
