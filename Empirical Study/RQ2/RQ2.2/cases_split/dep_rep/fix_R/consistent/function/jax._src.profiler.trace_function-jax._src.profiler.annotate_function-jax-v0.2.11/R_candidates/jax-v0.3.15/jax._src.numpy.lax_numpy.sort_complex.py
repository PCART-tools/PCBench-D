@_wraps(np.sort_complex)
@jit
def sort_complex(a):
  _check_arraylike("sort_complex", a)
  a = lax.sort(a, dimension=0)
  return lax.convert_element_type(a, dtypes._to_complex_dtype(a.dtype))
