  def bind(self, *args, **params):
    assert (not config.enable_checks.value or
            all(isinstance(arg, Tracer) or valid_jaxtype(arg) for arg in args)), args
    return self.bind_with_trace(find_top_trace(args), args, params)
