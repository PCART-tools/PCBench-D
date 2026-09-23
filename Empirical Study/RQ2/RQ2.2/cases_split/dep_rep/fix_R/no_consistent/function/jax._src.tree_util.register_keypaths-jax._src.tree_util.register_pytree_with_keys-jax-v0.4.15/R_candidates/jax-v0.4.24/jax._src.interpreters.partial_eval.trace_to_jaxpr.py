@profiler.annotate_function
def trace_to_jaxpr(
    fun: lu.WrappedFun, pvals: Sequence[PartialVal],
    instantiate: bool | Sequence[bool] = False,
  ) -> tuple[Jaxpr, list[PartialVal], list[core.Value]]:
  """
  Partially evaluate a function, building a jaxpr for un-evaluated computation.

  Args:
    fun: lu.WrappedFun representing the function to be partially evaluated. The
      function must be flattened, in the sense of accepting jaxpr type arguments
      and returning a flat list of jaxpr type outputs.
    pvals: sequence of PartialVals of length equal to the number of inputs to
      `fun` indicating which inputs are known or unknown.
    instantiate: optional bool or sequence of bools of length equal to the
      number of outputs of `fun` indicating which outputs should be forced to be
      treated as unknown and hence instantiated in the jaxpr. If a single bool,
      the value is applied to all outputs. Default False.

  Returns:
    A triple where the first element is a jaxpr representing the computation
    which depends on unknown inputs; the second element is a list of PartialVals
    of length equal to the length of the output of `fun` representing which
    outputs are known and unknown (along with their values and abstract values,
    respectively); the third element is a list of known residual values. The
    returned jaxpr takes as inputs the known residual values followed by values
    of the originally unknown inputs.
  """
  current_name_stack = source_info_util.current_name_stack()
  with core.new_main(JaxprTrace, name_stack=current_name_stack) as main:
    fun = trace_to_subjaxpr(fun, main, instantiate)
    jaxpr, (out_pvals, consts, env) = fun.call_wrapped(pvals)
    assert not env
    del main, fun, env

  return jaxpr, out_pvals, consts
