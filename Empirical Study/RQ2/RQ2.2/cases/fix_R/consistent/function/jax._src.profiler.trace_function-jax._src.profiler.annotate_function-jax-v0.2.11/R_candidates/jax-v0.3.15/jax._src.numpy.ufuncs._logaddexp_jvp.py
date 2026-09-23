@logaddexp.defjvp
def _logaddexp_jvp(primals, tangents):
  x1, x2 = primals
  t1, t2 = tangents
  x1, x2, t1, t2 = _promote_args_inexact("logaddexp_jvp", x1, x2, t1, t2)
  primal_out = logaddexp(x1, x2)
  tangent_out = lax.add(lax.mul(t1, exp(lax.sub(_replace_inf(x1), _replace_inf(primal_out)))),
                        lax.mul(t2, exp(lax.sub(_replace_inf(x2), _replace_inf(primal_out)))))
  return primal_out, tangent_out
