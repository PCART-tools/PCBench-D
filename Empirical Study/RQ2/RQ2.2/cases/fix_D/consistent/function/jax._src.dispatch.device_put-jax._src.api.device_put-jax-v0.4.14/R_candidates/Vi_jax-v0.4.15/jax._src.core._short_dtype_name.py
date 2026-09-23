def _short_dtype_name(dtype) -> str:
  if dtypes.issubdtype(dtype, dtypes.extended):
    return str(dtype)
  else:
    return (dtype.name.replace('float', 'f').replace('uint'   , 'u')
                      .replace('int'  , 'i').replace('complex', 'c'))
