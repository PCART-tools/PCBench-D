@weakref_lru_cache
def _transpose_jaxpr(jaxpr, in_lin, out_zeros, reduce_axes):
  in_avals = ([a for a,  lin in zip(jaxpr.in_avals,  in_lin   ) if not lin] +
              [a for a, zero in zip(jaxpr.out_avals, out_zeros) if not zero])
  cell = lambda: None

  @lu.wrap_init
  def transposed(*args_flat):
    ins_flat, out_cts_flat = split_list(args_flat, [len(in_lin) - sum(in_lin)])

    # Evaluate nonlinear parts using partial evaluation to get a linear jaxpr.
    ins_iter = iter(ins_flat)
    in_pvals = [pe.PartialVal.unknown(aval) if lin else
                pe.PartialVal.known(next(ins_iter))
                for aval, lin in zip(jaxpr.in_avals, in_lin)]
    assert next(ins_iter, None) is None
    lin_jaxpr, _, consts = pe.trace_to_jaxpr_nounits(
        lu.wrap_init(core.jaxpr_as_fun(jaxpr)), in_pvals, False)

    # Transpose the linear jaxpr (which only has linear inputs).
    out_cts_iter = iter(out_cts_flat)
    out_cts = [ad_util.Zero(aval) if zero else next(out_cts_iter)
               for aval, zero in zip(jaxpr.out_avals, out_zeros)]
    assert next(out_cts_iter, None) is None
    dummy_args = [ad.UndefinedPrimal(v.aval) for v in lin_jaxpr.invars]
    in_cts = ad.backward_pass(lin_jaxpr, reduce_axes, False, consts, dummy_args,
                              out_cts)

    # Identify symbolic zeros in the resulting cotangents, and return nonzeros.
    in_zeros = cell.in_cts_zero = [type(ct) is ad_util.Zero for ct in in_cts]
    in_cts_nz, _ = partition_list(in_zeros, in_cts)
    return in_cts_nz

  transposed_jaxpr_, _, consts = pe.trace_to_jaxpr_dynamic(transposed, in_avals)
  transposed_jaxpr = core.ClosedJaxpr(transposed_jaxpr_, consts)
  return transposed_jaxpr, cell.in_cts_zero  # type: ignore
