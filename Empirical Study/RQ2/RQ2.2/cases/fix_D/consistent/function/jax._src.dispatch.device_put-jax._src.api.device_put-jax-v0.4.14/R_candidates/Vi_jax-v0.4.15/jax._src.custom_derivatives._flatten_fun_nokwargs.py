@lu.transformation_with_aux
def _flatten_fun_nokwargs(in_tree, *args_flat):
  py_args = tree_unflatten(in_tree, args_flat)
  ans = yield py_args, {}
  ans_flat, ans_tree = tree_flatten(ans)
  ans_avals = [core.raise_to_shaped(core.get_aval(x)) for x in ans_flat]
  yield ans_flat, (ans_tree, ans_avals)
