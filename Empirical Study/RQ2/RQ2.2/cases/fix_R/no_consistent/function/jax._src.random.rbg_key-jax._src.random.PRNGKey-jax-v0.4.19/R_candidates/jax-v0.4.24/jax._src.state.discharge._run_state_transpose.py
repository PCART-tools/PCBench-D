def _run_state_transpose(in_cts, *args, jaxpr: core.Jaxpr,
                         which_linear: tuple[bool, ...]):
  # if any in_ct is nonzero, we definitely want it in args_ (and the
  # corresponding x in args could be an undefined primal, but doesn't have to be)
  # for non-res stuff:
  #   getting and setting => (nonzero ct, UndefinedPrimal arg)
  #   just setting =>        (nonzero ct, not UndefinedPrimal, dummy value)
  #   just getting =>        (zero ct   , UndefinedPrimal arg)
  # for res stuff:
  #                          (zero ct   , not UndefinedPrimal)
  assert any(which_linear)
  transpose_args = []
  for x, ct in zip(args, in_cts):
    if   type(ct) is     ad_util.Zero and not ad.is_undefined_primal(x):
      # this is a residual, take x!
      transpose_args.append(x)
    elif type(ct) is     ad_util.Zero and     ad.is_undefined_primal(x):
      # the loop was 'just getting', plug in a zero
      transpose_args.append(ad_util.zeros_like_aval(x.aval))
    elif type(ct) is not ad_util.Zero and not ad.is_undefined_primal(x):
      # the loop was 'just setting', grab that cotangent! x is dummy
      transpose_args.append(ct)
    elif type(ct) is not ad_util.Zero and     ad.is_undefined_primal(x):
      # the loop was 'getting and setting', grab that cotangent!
      transpose_args.append(ct)
  jaxpr_transpose_, consts = _transpose_jaxpr(jaxpr, which_linear)
  jaxpr_transpose = hoist_consts_to_refs(jaxpr_transpose_)
  which_linear = (*[False] * len(consts), *which_linear)
  const_all_outs = run_state_p.bind(*consts, *transpose_args,
                                    jaxpr=jaxpr_transpose,
                                    which_linear=which_linear)
  _, all_outs = split_list(const_all_outs, [len(consts)])
  ct_outs = [ct if ad.is_undefined_primal(x) else None
             for x, ct in zip(args, all_outs)]
  return ct_outs
