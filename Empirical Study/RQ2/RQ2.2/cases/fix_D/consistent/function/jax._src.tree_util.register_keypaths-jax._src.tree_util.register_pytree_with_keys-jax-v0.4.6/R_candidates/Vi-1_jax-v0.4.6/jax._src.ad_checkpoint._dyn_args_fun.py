@weakref_lru_cache
def _dyn_args_fun(fun: Callable, static_argnums: FrozenSet[int],
                  static_args: Tuple[WrapHashably, ...], nargs: int):
  def new_fun(*dyn_args, **kwargs):
    static_args_, dyn_args_ = iter(static_args), iter(dyn_args)
    full_args = [next(static_args_).val if i in static_argnums
                 else next(dyn_args_) for i in range(nargs)]
    return fun(*full_args, **kwargs)
  return new_fun
