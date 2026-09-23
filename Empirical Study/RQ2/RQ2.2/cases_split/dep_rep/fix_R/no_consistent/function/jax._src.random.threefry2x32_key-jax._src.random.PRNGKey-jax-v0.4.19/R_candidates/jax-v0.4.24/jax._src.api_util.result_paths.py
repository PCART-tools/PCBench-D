@lu.transformation_with_aux
def result_paths(*args, **kwargs):
  "linear_util transform to get output pytree paths of pre-flattened function."
  ans = yield args, kwargs
  yield ans, [keystr(path) for path, _ in generate_key_paths(ans)]
