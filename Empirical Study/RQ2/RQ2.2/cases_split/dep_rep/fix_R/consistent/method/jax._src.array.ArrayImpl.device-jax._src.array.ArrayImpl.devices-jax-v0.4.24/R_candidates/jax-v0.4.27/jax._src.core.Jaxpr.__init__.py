  def __init__(self, constvars: Sequence[Var], invars: Sequence[Var],
               outvars: Sequence[Atom], eqns: Sequence[JaxprEqn],
               effects: Effects = no_effects,
               debug_info: JaxprDebugInfo | None = None):
    """
    Args:
      constvars: list of variables introduced for constants. Array constants are
        replaced with such variables while scalar constants are kept inline.
      invars: list of input variables. Together, `constvars` and `invars` are
        the inputs to the Jaxpr.
      outvars: list of output atoms.
      eqns: list of equations.
      effects: set of effects. The effects on a jaxpr are a superset of the
        union of the effects for each equation.
      debug_info: optional JaxprDebugInfo.
    """
    self._constvars = list(constvars)
    self._invars = list(invars)
    self._outvars = list(outvars)
    self._eqns = list(eqns)
    self._effects = effects
    self._debug_info = debug_info
    assert (not debug_info or len(debug_info.arg_names) == len(invars) and
            len(debug_info.result_paths) == len(outvars))
