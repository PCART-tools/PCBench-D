@_wraps(osp_special.digamma, module='scipy.special', lax_description="""\
The JAX version only accepts real-valued inputs.""")
def digamma(x):
  x, = _promote_args_inexact("digamma", x)
  return lax.digamma(x)
