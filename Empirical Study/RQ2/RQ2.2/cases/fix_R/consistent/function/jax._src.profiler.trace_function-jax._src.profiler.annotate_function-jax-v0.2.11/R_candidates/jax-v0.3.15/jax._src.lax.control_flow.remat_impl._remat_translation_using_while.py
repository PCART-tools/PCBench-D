def _remat_translation_using_while(*args,
                                   jaxpr: core.Jaxpr):
  # Implements:
  #  for(counter=0, result=0; counter < rng(1, 2); counter ++) {
  #     result = eval_jaxpr(*args)
  #  }
  # The loop carry is a tuple: (counter, result, args)
  avals_out = tuple(ov.aval for ov in jaxpr.outvars)
  dummies_like_result = tuple(_map(_dummy_remat_result, avals_out))
  carry_init = (np.int32(0), dummies_like_result, args)
  def cond(carry):
    counter, _, _ = carry
    return counter < lax.rng_uniform(np.int32(1), np.int32(2), shape=())

  def body(carry):
    counter, _, args = carry
    results = core.eval_jaxpr(jaxpr, (), *args)
    return (counter + 1, tuple(results), args)

  carry_res = while_loop(cond, body, carry_init)
  return carry_res[1]
