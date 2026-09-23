  def new_instantiated_literal(self, val) -> JaxprTracer:
    aval = get_aval(val)
    return JaxprTracer(self, PartialVal.unknown(aval),
                       Literal(val, raise_to_shaped(aval)))
