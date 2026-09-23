@_wraps(np.piecewise, lax_description=_PIECEWISE_DOC)
def piecewise(x, condlist, funclist, *args, **kw):
  _check_arraylike("piecewise", x)
  condlist = array(condlist, dtype=bool_)
  nc, nf = len(condlist), len(funclist)
  if nf == nc + 1:
    funclist = funclist[-1:] + funclist[:-1]
  elif nf == nc:
    funclist = [0] + list(funclist)
  else:
    raise ValueError(f"with {nc} condition(s), either {nc} or {nc+1} functions are expected; got {nf}")
  consts = {i: c for i, c in enumerate(funclist) if not callable(c)}
  funcs = {i: f for i, f in enumerate(funclist) if callable(f)}
  return _piecewise(x, condlist, consts,
                    frozenset(funcs.items()),  # dict is not hashable.
                    *args, **kw)
