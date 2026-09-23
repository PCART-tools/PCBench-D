def jvp(fun: lu.WrappedFun, has_aux=False, instantiate=True,
    transform_stack=True) -> Any:
  if not has_aux:
    return jvpfun(jvp_subtrace(fun), instantiate, transform_stack)
  else:
    fun, aux = jvp_subtrace_aux(fun)
    return jvpfun(fun, instantiate, transform_stack), aux
