  def dyn_args_maker(self, rng: Rng) -> Sequence:
    """A dynamic-argument maker, for use with `dyn_fun`."""
    return [
        self._arg_maker(ad, rng)
        for ad in self.arg_descriptors
        if not isinstance(ad, StaticArg)
    ]
