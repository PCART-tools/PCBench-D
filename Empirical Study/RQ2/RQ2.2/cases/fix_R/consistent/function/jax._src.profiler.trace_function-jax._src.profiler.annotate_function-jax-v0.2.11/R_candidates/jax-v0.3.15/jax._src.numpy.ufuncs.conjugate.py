@_wraps(np.conjugate, module='numpy')
@partial(jit, inline=True)
def conjugate(x):
  _check_arraylike("conjugate", x)
  return lax.conj(x) if np.iscomplexobj(x) else x
