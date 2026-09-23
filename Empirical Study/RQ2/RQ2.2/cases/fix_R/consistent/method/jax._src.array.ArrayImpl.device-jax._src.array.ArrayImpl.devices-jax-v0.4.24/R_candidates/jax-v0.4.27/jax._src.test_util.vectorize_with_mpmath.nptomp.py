  def nptomp(self, x):
    """Convert numpy array/scalar to an array/instance of mpmath number type.
    """
    if isinstance(x, np.ndarray):
      return np.fromiter(map(self.nptomp, x.flatten()), dtype=object).reshape(x.shape)
    elif isinstance(x, np.floating):
      mpmath = self.mpmath
      ctx = self.get_context(x)
      prec, rounding = ctx._prec_rounding
      if np.isposinf(x):
        return ctx.make_mpf(mpmath.libmp.finf)
      elif np.isneginf(x):
        return ctx.make_mpf(mpmath.libmp.fninf)
      elif np.isnan(x):
        return ctx.make_mpf(mpmath.libmp.fnan)
      elif np.isfinite(x):
        mantissa, exponent = np.frexp(x)
        man = int(np.ldexp(mantissa, prec))
        exp = int(exponent - prec)
        r = ctx.make_mpf(mpmath.libmp.from_man_exp(man, exp, prec, rounding))
        assert ctx.isfinite(r), r._mpf_
        return r
    elif isinstance(x, np.complexfloating):
      re, im = self.nptomp(x.real), self.nptomp(x.imag)
      return re.context.make_mpc((re._mpf_, im._mpf_))
    raise NotImplementedError(f'convert {type(x).__name__} instance to mpmath number type')
