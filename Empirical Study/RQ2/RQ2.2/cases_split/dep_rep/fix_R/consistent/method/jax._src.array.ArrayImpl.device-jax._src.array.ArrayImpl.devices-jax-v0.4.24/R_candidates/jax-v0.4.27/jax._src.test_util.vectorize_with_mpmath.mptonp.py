  def mptonp(self, x):
    """Convert mpmath instance to numpy array/scalar type.
    """
    if isinstance(x, np.ndarray) and x.dtype.kind == 'O':
      x_flat = x.flatten()
      item = x_flat[0]
      ctx = item.context
      fp_format = self.contexts_inv[ctx]
      if isinstance(item, ctx.mpc):
        dtype = getattr(np, self.map_float_to_complex[fp_format])
      elif isinstance(item, ctx.mpf):
        dtype = getattr(np, fp_format)
      else:
        dtype = None
      if dtype is not None:
        return np.fromiter(map(self.mptonp, x_flat), dtype=dtype).reshape(x.shape)
    elif isinstance(x, self.mpmath.ctx_mp.mpnumeric):
      ctx = x.context
      if isinstance(x, ctx.mpc):
        fp_format = self.contexts_inv[ctx]
        dtype = getattr(np, self.map_float_to_complex[fp_format])
        r = dtype().reshape(1).view(getattr(np, fp_format))
        r[0] = self.mptonp(x.real)
        r[1] = self.mptonp(x.imag)
        return r.view(dtype)[0]
      elif isinstance(x, ctx.mpf):
        fp_format = self.contexts_inv[ctx]
        dtype = getattr(np, fp_format)
        if ctx.isfinite(x):
          sign, man, exp, bc = self.mpmath.libmp.normalize(*x._mpf_, *ctx._prec_rounding)
          assert bc >= 0, (sign, man, exp, bc, x._mpf_)
          if exp + bc < self.float_minexp[fp_format]:
            return -ctx.zero if sign else ctx.zero
          if exp + bc > self.float_maxexp[fp_format]:
            return ctx.ninf if sign else ctx.inf
          man = dtype(-man if sign else man)
          r = np.ldexp(man, exp)
          assert np.isfinite(r), (x, r, x._mpf_, man)
          return r
        elif ctx.isnan(x):
          return dtype(np.nan)
        elif ctx.isinf(x):
          return dtype(-np.inf if x._mpf_[0] else np.inf)
    raise NotImplementedError(f'convert {type(x)} instance to numpy floating point type')
