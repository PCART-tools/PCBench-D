@dataclasses.dataclass
class CustomVJPPrimal:
  """Primal to a ``custom_vjp``'s forward rule when ``symbolic_zeros`` is set"""
  value: Any
  perturbed: bool
