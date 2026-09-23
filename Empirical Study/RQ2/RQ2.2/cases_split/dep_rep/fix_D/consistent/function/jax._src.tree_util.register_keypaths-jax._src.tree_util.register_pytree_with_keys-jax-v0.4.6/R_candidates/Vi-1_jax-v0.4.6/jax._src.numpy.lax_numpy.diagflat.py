@util._wraps(np.diagflat, lax_description=_SCALAR_VALUE_DOC)
def diagflat(v, k=0):
  util._check_arraylike("diagflat", v)
  v = ravel(v)
  v_length = len(v)
  adj_length = v_length + _abs(k)
  res = zeros(adj_length*adj_length, dtype=v.dtype)
  i = arange(0, adj_length-_abs(k))
  if (k >= 0):
    fi = i+k+i*adj_length
  else:
    fi = i+(i-k)*adj_length
  res = res.at[fi].set(v)
  res = res.reshape(adj_length, adj_length)
  return res
