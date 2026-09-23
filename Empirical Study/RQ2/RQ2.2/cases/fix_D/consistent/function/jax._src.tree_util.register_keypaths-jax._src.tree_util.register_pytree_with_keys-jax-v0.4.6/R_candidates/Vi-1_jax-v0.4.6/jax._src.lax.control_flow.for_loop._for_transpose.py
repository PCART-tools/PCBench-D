def _for_transpose(in_cts, *args, jaxpr, nsteps, reverse, which_linear, unroll):
  # if any in_ct is nonzero, we definitely want it in args_ (and the
  # corresponding x in args could be an undefined primal, but doesnt have to be)
  # for non-res stuff:
  #   getting and setting => (nonzero ct, UndefinedPrimal arg)
  #   just setting =>        (nonzero ct, not UndefinedPrimal, dummy value)
  #   just getting =>        (zero ct   , UndefinedPrimal arg)
  # for res stuff:
  #                          (zero ct   , not UndefinedPrimal)
  args_ = []
  which_linear_transpose = []
  for x, ct in zip(args, in_cts):
    if   type(ct) is     ad_util.Zero and not ad.is_undefined_primal(x):
      # this is a residual, take x!
      args_.append(x)
      which_linear_transpose.append(False)
    elif type(ct) is     ad_util.Zero and     ad.is_undefined_primal(x):
      # the loop was 'just getting', plug in a zero
      args_.append(ad_util.zeros_like_aval(x.aval))
      which_linear_transpose.append(False)
    elif type(ct) is not ad_util.Zero and not ad.is_undefined_primal(x):
      # the loop was 'just setting', grab that cotangent! x is dummy
      args_.append(ct)
      which_linear_transpose.append(False)
    elif type(ct) is not ad_util.Zero and     ad.is_undefined_primal(x):
      # the loop was 'getting and setting', grab that cotangent!
      args_.append(ct)
      which_linear_transpose.append(True)

  jaxpr_transpose = transpose_jaxpr(jaxpr, which_linear)
  assert len(args_) == len(jaxpr_transpose.invars) - 1
  all_outs = for_p.bind(*args_, jaxpr=jaxpr_transpose, nsteps=nsteps,
                        reverse=not reverse,
                        which_linear=tuple(which_linear_transpose),
                        unroll=unroll)
  ct_outs = [ct if ad.is_undefined_primal(x) else None
             for x, ct in zip(args, all_outs)]
  return ct_outs
