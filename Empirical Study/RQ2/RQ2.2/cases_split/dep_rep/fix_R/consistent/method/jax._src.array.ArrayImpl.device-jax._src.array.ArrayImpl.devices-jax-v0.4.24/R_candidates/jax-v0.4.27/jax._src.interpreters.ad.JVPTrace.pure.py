  def pure(self, val):
    tangent_zero = Zero(get_aval(val).at_least_vspace())
    return JVPTracer(self, val, tangent_zero)
