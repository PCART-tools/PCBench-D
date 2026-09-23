@curry
def transformation_with_aux(gen, fun: WrappedFun, *gen_static_args,
                            use_eq_store=False) -> tuple[WrappedFun, Any]:
  """Adds one more transformation with auxiliary output to a WrappedFun."""
  out_store = Store() if not use_eq_store else EqualStore()
  out_thunk = lambda: out_store.val
  return fun.wrap(gen, gen_static_args, out_store), out_thunk
