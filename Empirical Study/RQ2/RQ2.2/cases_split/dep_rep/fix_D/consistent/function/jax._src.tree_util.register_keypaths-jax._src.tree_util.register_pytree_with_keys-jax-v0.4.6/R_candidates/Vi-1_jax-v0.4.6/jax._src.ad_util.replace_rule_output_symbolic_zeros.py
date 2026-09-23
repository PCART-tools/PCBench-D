def replace_rule_output_symbolic_zeros(
    x: Union[JaxTypeOrTracer, SymbolicZero]) -> Union[JaxTypeOrTracer, Zero]:
  return Zero(x.aval) if type(x) is SymbolicZero else x
