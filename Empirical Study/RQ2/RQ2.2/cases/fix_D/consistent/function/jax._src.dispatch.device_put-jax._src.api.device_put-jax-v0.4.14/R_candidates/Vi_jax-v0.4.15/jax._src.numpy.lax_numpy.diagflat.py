@util._wraps(np.diagflat, lax_description=_SCALAR_VALUE_DOC)
def diagflat(v: ArrayLike, k: int = 0) -> Array:
  util.check_arraylike("diagflat", v)
  v_ravel = ravel(v)
  v_length = len(v_ravel)
  adj_length = v_length + abs(k)
  res = zeros(adj_length*adj_length, dtype=v_ravel.dtype)
  i = arange(0, adj_length-abs(k))
  if (k >= 0):
    fi = i+k+i*adj_length
  else:
    fi = i+(i-k)*adj_length
  res = res.at[fi].set(v_ravel)
  res = res.reshape(adj_length, adj_length)
  return res
