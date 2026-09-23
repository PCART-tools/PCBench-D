  def log1p(self, x):
    ctx = x.context
    if isinstance(x, ctx.mpc):
      # Workaround mpmath 1.3 bug in log(+-inf+-infj) evaluation (see mpmath/mpmath#774).
      # TODO(pearu): remove this function when mpmath 1.4 or newer
      # will be the required test dependency.
      if ctx.isinf(x.real) and ctx.isinf(x.imag):
        pi = ctx.pi
        if x.real > 0 and x.imag > 0:
          return ctx.make_mpc((x.real._mpf_, (pi / 4)._mpf_))
        if x.real > 0 and x.imag < 0:
          return ctx.make_mpc((x.real._mpf_, (-pi / 4)._mpf_))
        if x.real < 0 and x.imag < 0:
          return ctx.make_mpc(((-x.real)._mpf_, (-3 * pi / 4)._mpf_))
        if x.real < 0 and x.imag > 0:
          return ctx.make_mpc(((-x.real)._mpf_, (3 * pi / 4)._mpf_))
    return ctx.log1p(x)
