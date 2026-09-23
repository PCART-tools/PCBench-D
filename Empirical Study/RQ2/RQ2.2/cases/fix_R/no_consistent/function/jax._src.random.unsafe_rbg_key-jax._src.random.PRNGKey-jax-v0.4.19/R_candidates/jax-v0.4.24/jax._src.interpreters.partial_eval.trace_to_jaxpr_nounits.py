@profiler.annotate_function
def trace_to_jaxpr_nounits(
    fun: lu.WrappedFun, pvals: Sequence[PartialVal],
    instantiate: bool | Sequence[bool] = False,
  ) -> tuple[Jaxpr, list[PartialVal], list[core.Value]]:
  current_name_stack = source_info_util.current_name_stack()
  with core.new_main(JaxprTrace, name_stack=current_name_stack) as main:
    fun = trace_to_subjaxpr_nounits(fun, main, instantiate)
    jaxpr, (out_pvals, consts, env) = fun.call_wrapped(pvals)
    assert not env
    del main, fun, env
  return jaxpr, out_pvals, consts
