  def tan(self, x):
    ctx = x.context
    if isinstance(x, ctx.mpc):
      # Workaround mpmath 1.3 bug in tan(+-inf+-infj) evaluation (see mpmath/mpmath#781).
      # TODO(pearu): remove this function when mpmath 1.4 or newer
      # will be the required test dependency.
      if ctx.isinf(x.imag) and (ctx.isinf(x.real) or ctx.isfinite(x.real)):
        if x.imag > 0:
          return ctx.make_mpc((ctx.zero._mpf_, ctx.one._mpf_))
        return ctx.make_mpc((ctx.zero._mpf_, (-ctx.one)._mpf_))
      if ctx.isinf(x.real) and ctx.isfinite(x.imag):
        return ctx.make_mpc((ctx.nan._mpf_, ctx.nan._mpf_))
    return ctx.tan(x)
