@lu.transformation_with_aux
def _flatten_and_get_error_metadata_thunk(*invals):
  error, out = yield invals, {}
  out_vals, out_tree = jtu.tree_flatten((error, out))
  yield out_vals, (out_tree, set(error._pred.keys()))
