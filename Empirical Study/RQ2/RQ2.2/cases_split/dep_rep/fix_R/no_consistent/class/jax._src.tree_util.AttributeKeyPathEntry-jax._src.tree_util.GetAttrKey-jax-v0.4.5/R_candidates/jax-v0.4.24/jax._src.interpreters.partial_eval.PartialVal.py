class PartialVal(tuple):
  """Partial value: either a known value or an unknown (abstract) value.

  Represented as a pair `(aval_opt, const)` of one of two kinds:
  * `(None, <Constant>)` indicates a known value, where the constant is either a
    Tracer or satisfies `core.valid_jaxtype(const)`;
  * `(<AbstractValue>, None)` indicates an unknown value characterized by an
    abstract value.
  """
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

  @classmethod
  def known(cls, const: core.Value) -> PartialVal:
    return PartialVal((None, const))

  @classmethod
  def unknown(cls, aval: AbstractValue) -> PartialVal:
    return PartialVal((aval, None))

  def is_known(self) -> bool:
    return self[0] is None

  def get_known(self) -> core.Value | None:
    """Get the known value, if known, else None."""
    return self[1] if self[0] is None else None

  def get_aval(self) -> AbstractValue:
    """Get AbstractValue directly (if unknown) or from the constant (known)."""
    known = self.get_known()
    if known is not None:
      return get_aval(known)
    else:
      return self[0]
