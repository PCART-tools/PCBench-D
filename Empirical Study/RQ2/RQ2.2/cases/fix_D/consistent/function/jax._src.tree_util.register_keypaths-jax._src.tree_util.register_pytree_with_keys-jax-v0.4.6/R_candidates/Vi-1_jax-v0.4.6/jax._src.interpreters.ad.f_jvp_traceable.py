@lu.transformation_with_aux
def f_jvp_traceable(nonzeros, *primals_and_nztangents):
  num_primals = len(nonzeros)
  primals = list(primals_and_nztangents[:num_primals])
  nonzero_tangents = iter(primals_and_nztangents[num_primals:])
  tangents = [next(nonzero_tangents) if nz else Zero.from_value(p)
              for p, nz in zip(primals, nonzeros)]
  primals_out, tangents_out = yield (primals, tangents), {}
  out_nonzeros = [type(t) is not Zero for t in tangents_out]
  nonzero_tangents_out = [t for t in tangents_out if type(t) is not Zero]
  yield list(primals_out) + nonzero_tangents_out, out_nonzeros
