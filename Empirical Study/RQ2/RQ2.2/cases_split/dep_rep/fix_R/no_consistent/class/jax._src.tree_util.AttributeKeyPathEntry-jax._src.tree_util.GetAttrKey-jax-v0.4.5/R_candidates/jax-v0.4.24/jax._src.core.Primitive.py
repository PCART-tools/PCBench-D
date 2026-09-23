class Primitive:
  name: str
  # set for multi-output primitives.
  multiple_results: bool = False
  # set for call primitives processed in final style.
  call_primitive: bool = False
  # set for map primitives processed in final style.
  map_primitive: bool = False

  def __init__(self, name: str):
    self.name = name

  def __repr__(self):
    return f'{self.name}'

  def bind(self, *args, **params):
    assert (not config.enable_checks.value or
            all(isinstance(arg, Tracer) or valid_jaxtype(arg) for arg in args)), args
    return self.bind_with_trace(find_top_trace(args), args, params)

  def bind_with_trace(self, trace, args, params):
    out = trace.process_primitive(self, map(trace.full_raise, args), params)
    return map(full_lower, out) if self.multiple_results else full_lower(out)

  def def_impl(self, impl):
    self.impl = impl
    return impl

  def def_abstract_eval(self, abstract_eval):
    self.abstract_eval = _effect_free_abstract_eval(abstract_eval)  # type: ignore[assignment]
    return abstract_eval

  def def_effectful_abstract_eval(self, effectful_abstract_eval):
    self.abstract_eval = effectful_abstract_eval  # type: ignore[assignment]
    return effectful_abstract_eval

  def def_custom_bind(self, bind):
    self.bind = bind
    return bind

  def impl(self, *args, **params):
    raise NotImplementedError("Evaluation rule for '{}' not implemented"
                              .format(self.name))

  def abstract_eval(self, *args, **params):
    raise NotImplementedError("Abstract evaluation for '{}' not implemented"
                              .format(self.name))

  def get_bind_params(self, params):
    return [], params
