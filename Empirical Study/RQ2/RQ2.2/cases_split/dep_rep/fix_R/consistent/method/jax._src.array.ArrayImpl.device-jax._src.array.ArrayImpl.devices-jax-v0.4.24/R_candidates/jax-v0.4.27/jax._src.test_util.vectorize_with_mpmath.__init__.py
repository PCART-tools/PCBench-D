  def __init__(self, *args, **kwargs):
    mpmath = kwargs.pop('mpmath', None)
    if mpmath is None:
      raise ValueError('vectorize_with_mpmath: no mpmath argument specified')
    self.extra_prec_multiplier = kwargs.pop('extra_prec_multiplier', 0)
    self.extra_prec = kwargs.pop('extra_prec', 0)
    self.mpmath = mpmath
    self.contexts = dict()
    self.contexts_inv = dict()
    for fp_format, prec in self.float_prec.items():
      ctx = self.mpmath.mp.clone()
      ctx.prec = prec
      self.contexts[fp_format] = ctx
      self.contexts_inv[ctx] = fp_format

    super().__init__(*args, **kwargs)
