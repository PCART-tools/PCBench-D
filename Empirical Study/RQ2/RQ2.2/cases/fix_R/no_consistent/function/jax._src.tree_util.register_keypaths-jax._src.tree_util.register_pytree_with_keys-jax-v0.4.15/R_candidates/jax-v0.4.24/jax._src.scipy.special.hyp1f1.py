@custom_derivatives.custom_jvp
@jit
@jnp.vectorize
@implements(osp_special.hyp1f1, module='scipy.special', lax_description="""\
The JAX version only accepts positive and real inputs. Values of a, b and x
leading to high values of 1F1 might be erroneous, considering enabling double
precision. Convention for a = b = 0 is 1, unlike in scipy's implementation.""")
def hyp1f1(a, b, x):
  """
  Implementation of the 1F1 hypergeometric function for real valued inputs
  Backed by https://doi.org/10.48550/arXiv.1407.7786
  There is room for improvement in the implementation using recursion to
  evaluate lower values of hyp1f1 when a or b or both are > 60-80
  """
  a, b, x = promote_args_inexact('hyp1f1', a, b, x)

  result = lax.cond(lax.abs(x) < 100, _hyp1f1_serie, _hyp1f1_asymptotic, a, b, x)
  index = (a == 0) * 1 + ((a == b) & (a != 0)) * 2 + ((b == 0) & (a != 0)) * 3

  return lax.select_n(index,
                      result,
                      jnp.array(1, dtype=x.dtype),
                      jnp.exp(x),
                      jnp.array(jnp.inf, dtype=x.dtype))
