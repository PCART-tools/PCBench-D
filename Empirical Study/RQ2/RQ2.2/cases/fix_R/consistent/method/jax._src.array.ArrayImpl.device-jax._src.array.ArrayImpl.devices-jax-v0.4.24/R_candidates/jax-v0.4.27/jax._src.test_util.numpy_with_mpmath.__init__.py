  def __init__(self, mpmath, extra_prec_multiplier=0, extra_prec=0):
    self.mpmath = mpmath

    for name in self._provides:
      mp_name = self._mp_names.get(name, name)

      if hasattr(self, name):
        op = getattr(self, name)
      else:

        def op(x, mp_name=mp_name):
          return getattr(x.context, mp_name)(x)

      setattr(self, name, vectorize_with_mpmath(op, mpmath=mpmath, extra_prec_multiplier=extra_prec_multiplier, extra_prec=extra_prec))
