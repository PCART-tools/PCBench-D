  def get_bind_params(self, params):
    new_params = dict(params)
    jaxpr = new_params.pop('call_jaxpr')
    subfun = lu.hashable_partial(lu.wrap_init(eval_jaxpr), jaxpr, ())
    if config.dynamic_shapes.value:
      subfun = lu.annotate(subfun, _jaxpr_type_to_callable_annotation(jaxpr))
    return [subfun], new_params
