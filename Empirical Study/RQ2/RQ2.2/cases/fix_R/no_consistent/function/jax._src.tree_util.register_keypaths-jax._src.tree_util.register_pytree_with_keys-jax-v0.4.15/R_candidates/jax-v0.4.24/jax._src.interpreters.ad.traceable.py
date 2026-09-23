@lu.transformation_with_aux
def traceable(in_tree, *primals_and_tangents):
  primals, tangents = tree_unflatten(in_tree, primals_and_tangents)
  tangents = [Zero(get_aval(p).at_least_vspace()) if t is None else t
              for p, t in zip(primals, tangents)]
  primals_out, tangents_out = yield (primals, tangents), {}
  tangents_out = [None if type(t) is Zero else t for t in tangents_out]
  out_flat, out_tree = tree_flatten((primals_out, tangents_out))
  yield out_flat, out_tree
