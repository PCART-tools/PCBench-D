@custom_jvp
def _det(a):
  sign, logdet = slogdet(a)
  return sign * ufuncs.exp(logdet).astype(sign.dtype)
