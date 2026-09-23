  def sqrt(self, x):
    ctx = x.context
    if isinstance(x, ctx.mpc):
      # Workaround mpmath 1.3 bug in sqrt(+-inf+-infj) evaluation (see mpmath/mpmath#776).
      # TODO(pearu): remove this function when mpmath 1.4 or newer
      # will be the required test dependency.
      if ctx.isinf(x.imag):
        return ctx.make_mpc((ctx.inf._mpf_, x.imag._mpf_))
    return ctx.sqrt(x)
