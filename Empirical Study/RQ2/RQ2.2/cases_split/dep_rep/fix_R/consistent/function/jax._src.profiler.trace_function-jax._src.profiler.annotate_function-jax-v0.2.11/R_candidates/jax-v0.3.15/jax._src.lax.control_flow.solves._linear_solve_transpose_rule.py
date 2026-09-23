def _linear_solve_transpose_rule(cotangent, *primals, const_lengths, jaxprs):
  if jaxprs.transpose_solve is None:
    raise TypeError('transpose_solve required for backwards mode automatic '
                    'differentiation of custom_linear_solve')

  params, b = _split_linear_solve_args(primals, const_lengths)
  # split off symbolic zeros in the cotangent if present
  x_cotangent, _ = split_list(cotangent, [len(b)])
  assert all(ad.is_undefined_primal(x) for x in b)
  cotangent_b_full = linear_solve_p.bind(
      *(_flatten(params.transpose()) + x_cotangent),
      const_lengths=const_lengths.transpose(), jaxprs=jaxprs.transpose())
  # drop aux values in cotangent computation
  cotangent_b, _ = split_list(cotangent_b_full, [len(b)])
  return [None] * sum(const_lengths) + cotangent_b
