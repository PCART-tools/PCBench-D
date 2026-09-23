  def arcsin(self, x):
    ctx = x.context
    if isinstance(x, ctx.mpc):
      # Workaround mpmath 1.3 bug in asin(+-inf+-infj) evaluation (see
      # mpmath/mpmath#793).
      # TODO(pearu): remove the if-block below when mpmath 1.4 or
      # newer will be the required test dependency.
      pi = ctx.pi
      inf = ctx.inf
      zero = ctx.zero
      if ctx.isinf(x.real):
        sign_real = -1 if x.real < 0 else 1
        real = sign_real * pi / (4 if ctx.isinf(x.imag) else 2)
        imag = -inf if x.imag < 0 else inf
        return ctx.make_mpc((real._mpf_, imag._mpf_))
      elif ctx.isinf(x.imag):
        return ctx.make_mpc((zero._mpf_, x.imag._mpf_))

      # On branch cut, mpmath.mp.asin returns different value compared
      # to mpmath.fp.asin and numpy.arcsin (see
      # mpmath/mpmath#786). The following if-block ensures
      # compatibiliy with numpy.arcsin.
      if x.real > 1 and x.imag == 0:
        return ctx.asin(x).conjugate()

    return ctx.asin(x)
