@lu.transformation_with_aux
def nonzero_outputs(*args, **kwargs):
  results = yield args, kwargs
  yield results, [type(r) is not Zero for r in results]
