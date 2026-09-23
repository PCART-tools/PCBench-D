@lu.transformation_with_aux
def nonzero_tangent_outputs(*args, **kwargs):
  results = (_, tangents_out) = yield args, kwargs
  yield results, [type(r) is not Zero for r in tangents_out]
