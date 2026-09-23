@lu.transformation
def jvpfun(instantiate, transform_stack, primals, tangents):
  tangents = [Zero.from_value(t) if not isinstance(t, Zero)
              and dtype(t) == float0 else t for t in tangents]
  ctx = (source_info_util.transform_name_stack('jvp') if transform_stack
         else contextlib.nullcontext())
  with core.new_main(JVPTrace) as main, ctx:
    out_primals, out_tangents = yield (main, primals, tangents), {}
    del main
  if type(instantiate) is bool:
    instantiate = [instantiate] * len(out_tangents)
  out_tangents = [instantiate_zeros(t) if inst else t for t, inst
                  in zip(out_tangents, instantiate)]
  yield out_primals, out_tangents
