@lu.transformation_with_aux
def flatten_fun_output(*args):
  ans = yield args, {}
  yield tree_flatten(ans)
