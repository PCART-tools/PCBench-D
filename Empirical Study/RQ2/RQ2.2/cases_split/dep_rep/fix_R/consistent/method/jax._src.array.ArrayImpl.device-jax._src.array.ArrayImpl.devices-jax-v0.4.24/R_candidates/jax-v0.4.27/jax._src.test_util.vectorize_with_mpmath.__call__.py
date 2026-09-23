  def __call__(self, *args, **kwargs):
    mp_args = []
    context = None
    for a in args:
      if isinstance(a, (np.ndarray, np.floating, np.complexfloating)):
        mp_args.append(self.nptomp(a))
        if context is None:
          context = self.get_context(a)
        else:
          assert context is self.get_context(a)
      else:
        mp_args.append(a)

    extra_prec = int(context.prec * self.extra_prec_multiplier) + self.extra_prec
    with context.extraprec(extra_prec):
      result = super().__call__(*mp_args, **kwargs)

    if isinstance(result, tuple):
      lst = []
      for r in result:
        if ((isinstance(r, np.ndarray) and r.dtype.kind == 'O')
            or isinstance(r, self.mpmath.ctx_mp.mpnumeric)):
          r = self.mptonp(r)
        lst.append(r)
      return tuple(lst)

    if ((isinstance(result, np.ndarray) and result.dtype.kind == 'O')
        or isinstance(result, self.mpmath.ctx_mp.mpnumeric)):
      return self.mptonp(result)

    return result
