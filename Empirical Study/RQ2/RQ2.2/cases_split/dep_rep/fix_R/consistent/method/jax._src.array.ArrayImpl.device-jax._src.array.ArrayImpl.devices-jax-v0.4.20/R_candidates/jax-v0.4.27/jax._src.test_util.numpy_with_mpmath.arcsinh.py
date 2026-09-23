  def arcsinh(self, x):
    ctx = x.context

    if isinstance(x, ctx.mpc):
      # Workaround mpmath 1.3 bug in asinh(+-inf+-infj) evaluation
      # (see mpmath/mpmath#749).
      # TODO(pearu): remove the if-block below when mpmath 1.4 or
      # newer will be the required test dependency.
      pi = ctx.pi
      inf = ctx.inf
      zero = ctx.zero
      if ctx.isinf(x.imag):
        sign_imag = -1 if x.imag < 0 else 1
        real = -inf if x.real < 0 else inf
        imag = sign_imag * pi / (4 if ctx.isinf(x.real) else 2)
        return ctx.make_mpc((real._mpf_, imag._mpf_))
      elif ctx.isinf(x.real):
        return ctx.make_mpc((x.real._mpf_, zero._mpf_))

      # On branch cut, mpmath.mp.asinh returns different value
      # compared to mpmath.fp.asinh and numpy.arcsinh (see
      # mpmath/mpmath#786).  The following if-block ensures
      # compatibiliy with numpy.arcsinh.
      if x.real == 0 and x.imag < -1:
        return (-ctx.asinh(x)).conjugate()
    return ctx.asinh(x)
