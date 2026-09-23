def remat_transpose(reduce_axes, out_cts, *in_primals, jaxpr, **params):
  assert not jaxpr.constvars
  in_linear = [ad.is_undefined_primal(x) for x in in_primals]
  out_zeros = [type(ct) is ad_util.Zero for ct in out_cts]
  transposed_jaxpr_, in_zeros = transpose_jaxpr(
      pe.close_jaxpr(jaxpr), in_linear, out_zeros, reduce_axes)
  transposed_jaxpr, consts = transposed_jaxpr_.jaxpr, transposed_jaxpr_.consts
  transposed_jaxpr = pe.convert_constvars_jaxpr(transposed_jaxpr)
  args, _ = tree_flatten((in_primals, out_cts))
  in_cts_nz = remat_p.bind(*consts, *args, jaxpr=transposed_jaxpr, **params)
  in_cts_nz_, in_zeros_ = iter(in_cts_nz), iter(in_zeros)
  in_cts = [None if not ad.is_undefined_primal(x) else
            ad_util.Zero(x.aval) if next(in_zeros_) else next(in_cts_nz_)
            for x in in_primals]
  assert next(in_cts_nz_, None) is next(in_zeros_, None) is None
  return in_cts
