def pp_aval(a: AbstractValue, context: JaxprPpContext) -> str:
  if isinstance(a, DShapedArray):
    shape = [pp_var(d, context) if type(d) is Var else str(d) for d in a.shape]
    dtype = _short_dtype_name(a.dtype)
    return f'{dtype}[{",".join(shape)}]'
  else:
    return a.str_short(short_dtypes=True)
