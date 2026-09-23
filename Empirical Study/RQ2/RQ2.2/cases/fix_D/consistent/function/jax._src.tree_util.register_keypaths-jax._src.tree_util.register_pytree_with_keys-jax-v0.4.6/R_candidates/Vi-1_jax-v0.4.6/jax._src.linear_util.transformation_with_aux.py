@curry
def transformation_with_aux(gen, fun: WrappedFun, *gen_static_args) -> Tuple[WrappedFun, Any]:
  """Adds one more transformation with auxiliary output to a WrappedFun."""
  out_store = Store()
  out_thunk = lambda: out_store.val
  return fun.wrap(gen, gen_static_args, out_store), out_thunk
