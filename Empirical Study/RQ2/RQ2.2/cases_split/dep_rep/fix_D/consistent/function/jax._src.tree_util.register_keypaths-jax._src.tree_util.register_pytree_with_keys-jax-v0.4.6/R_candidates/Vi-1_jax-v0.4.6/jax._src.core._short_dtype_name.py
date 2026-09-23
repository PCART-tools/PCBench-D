def _short_dtype_name(dtype) -> str:
  if type(dtype) in opaque_dtypes:
    return str(dtype)
  else:
    return (dtype.name.replace('float', 'f').replace('uint'   , 'u')
                      .replace('int'  , 'i').replace('complex', 'c'))
