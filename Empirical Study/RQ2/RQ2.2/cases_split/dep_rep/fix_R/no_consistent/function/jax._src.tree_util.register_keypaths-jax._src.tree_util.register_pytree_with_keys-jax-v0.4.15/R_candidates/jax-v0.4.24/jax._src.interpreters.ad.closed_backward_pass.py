def closed_backward_pass(jaxpr: core.ClosedJaxpr, reduce_axes, transform_stack,
                         primals_in, cotangents_in):
  return backward_pass(jaxpr.jaxpr, reduce_axes, transform_stack, jaxpr.consts,
                       primals_in, cotangents_in)
