  def __new__(cls, xs: tuple[AbstractValue | None, core.Value]):
    pv, const = xs
    if config.enable_checks.value:
      # type checks
      assert isinstance(pv, (AbstractValue, type(None))), xs
      assert (const is None or isinstance(const, core.Tracer) or
              core.valid_jaxtype(const)), const
      # invariant checks
      assert (pv is None) ^ (const is None)
    return tuple.__new__(cls, xs)
