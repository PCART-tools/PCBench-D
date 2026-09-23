@util._wraps(np.piecewise, lax_description=_PIECEWISE_DOC)
def piecewise(x: ArrayLike, condlist: Union[Array, Sequence[ArrayLike]],
              funclist: List[Union[ArrayLike, Callable[..., Array]]],
              *args, **kw) -> Array:
  util.check_arraylike("piecewise", x)
  nc, nf = len(condlist), len(funclist)
  if nf == nc + 1:
    funclist = funclist[-1:] + funclist[:-1]
  elif nf == nc:
    funclist = [0] + list(funclist)
  else:
    raise ValueError(f"with {nc} condition(s), either {nc} or {nc+1} functions are expected; got {nf}")
  consts = {i: c for i, c in enumerate(funclist) if not callable(c)}
  funcs = {i: f for i, f in enumerate(funclist) if callable(f)}
  return _piecewise(asarray(x), asarray(condlist, dtype=bool_), consts,
                    frozenset(funcs.items()),  # dict is not hashable.
                    *args, **kw)
