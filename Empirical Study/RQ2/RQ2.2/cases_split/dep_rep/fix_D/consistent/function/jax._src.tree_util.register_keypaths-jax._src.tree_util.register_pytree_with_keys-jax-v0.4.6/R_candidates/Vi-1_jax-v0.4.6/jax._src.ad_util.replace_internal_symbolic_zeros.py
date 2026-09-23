def replace_internal_symbolic_zeros(
    x: Union[JaxTypeOrTracer, Zero]) -> Union[JaxTypeOrTracer, SymbolicZero]:
  return SymbolicZero(x.aval) if type(x) is Zero else x
