def _conj_impl(x, **kw):
  if dtypes.issubdtype(x.dtype, np.complexfloating):
    return complex(real(x), -imag(x))
  else:
    return complex(x, _zeros(x))
