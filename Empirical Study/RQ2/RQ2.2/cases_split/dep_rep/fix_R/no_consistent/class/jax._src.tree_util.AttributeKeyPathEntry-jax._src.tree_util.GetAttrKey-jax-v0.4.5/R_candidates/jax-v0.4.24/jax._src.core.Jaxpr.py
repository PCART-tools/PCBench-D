class Jaxpr:
  __slots__ = ['__weakref__', '_constvars', '_invars', '_outvars', '_eqns',
               '_effects', '_debug_info']

  _constvars: list[Var]
  _invars: list[Var]
  _outvars: list[Atom]
  _eqns: list[JaxprEqn]
  _effects: Effects
  _debug_info: JaxprDebugInfo | None

  @property
  def constvars(self) -> list[Var]:
    return self._constvars

  @property
  def invars(self) -> list[Var]:
    return self._invars

  @property
  def outvars(self) -> list[Atom]:
    return self._outvars

  @property
  def eqns(self) -> list[JaxprEqn]:
    return self._eqns

  @property
  def effects(self) -> Effects:
    return self._effects

  @property
  def debug_info(self) -> JaxprDebugInfo | None:
    return self._debug_info

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

  def __str__(self):
    return str(self.pretty_print())

  __repr__ = __str__

  def pretty_print(self, *, source_info=False, print_shapes=True,
                   custom_pp_eqn_rules=True, name_stack=False,
                   print_effects: bool = False, **kwargs):
    context = JaxprPpContext()
    settings = JaxprPpSettings(
        source_info=source_info,
        print_shapes=print_shapes,
        custom_pp_eqn_rules=custom_pp_eqn_rules,
        name_stack=name_stack,
        print_effects=print_effects)

    # Compute how many times each jaxpr is used.
    names = defaultdict[Jaxpr, str](lambda: "jaxpr")
    jaxpr_counts = Counter[Jaxpr]()
    s = deque([self])
    while s:
      jaxpr = s.popleft()
      jaxpr_counts[jaxpr] += 1
      for eqn in jaxpr.eqns:
        # TODO(slebedev): Come up with a more elaborate heuristic for name=.
        name = eqn.params.get("name")
        if name is None:
          s.extend(jaxprs_in_params(eqn.params))
          continue
        name = name.strip("<>")  # <lambda> -> lambda
        for subjaxpr in jaxprs_in_params(eqn.params):
          s.append(subjaxpr)
          names.setdefault(subjaxpr, name)

    # Pull jaxprs occurring more than once to the top-level, making sure
    # that their names are unique.
    docs = []
    name_counts = Counter[str]()
    for jaxpr, c in jaxpr_counts.items():
      if c == 1:
        continue
      name = names[jaxpr]
      if (count := name_counts[name]) > 0:
        name_counts[name] += 1
        name += str(count)
        name_counts[name] += 1
      else:
        name_counts[name] += 1
      docs.append(pp_top_level_jaxpr(name, jaxpr, context, settings))
      context.used_names.add(name)
      context.top_level_jaxprs[jaxpr] = name
    docs.append(pp_jaxpr(self, context, settings))
    return pp.concat(docs).format(**kwargs)

  def _repr_pretty_(self, p, cycle):
    return p.text(self.pretty_print(use_color=True))

  def replace(self, *, constvars=None, invars=None, outvars=None, eqns=None,
              effects=None, debug_info=None):
    constvars = self.constvars if constvars is None else constvars
    invars =  self.invars if invars is None else invars
    outvars = self.outvars if outvars is None else outvars
    eqns = self.eqns if eqns is None else eqns
    effects = self.effects if effects is None else effects
    return Jaxpr(constvars=constvars, invars=invars, outvars=outvars, eqns=eqns,
                 effects=effects, debug_info=debug_info)
