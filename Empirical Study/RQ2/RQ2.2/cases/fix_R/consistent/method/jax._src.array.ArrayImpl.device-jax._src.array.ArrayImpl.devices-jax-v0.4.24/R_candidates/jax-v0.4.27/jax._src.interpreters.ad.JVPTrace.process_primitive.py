  def process_primitive(self, primitive, tracers, params):
    primals_in, tangents_in = unzip2((t.primal, t.tangent) for t in tracers)
    jvp = primitive_jvps.get(primitive)
    if not jvp:
      msg = f"Differentiation rule for '{primitive}' not implemented"
      raise NotImplementedError(msg)
    primal_out, tangent_out = jvp(primals_in, tangents_in, **params)
    if primitive.multiple_results:
      return [JVPTracer(self, x, t) for x, t in zip(primal_out, tangent_out)]
    else:
      return JVPTracer(self, primal_out, tangent_out)
