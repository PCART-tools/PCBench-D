def emit_pipeline(
    body: PipelineBody,
    *,
    grid: core.StaticGrid,
    in_specs: PipelineBlockSpecs,
    out_specs: PipelineBlockSpecs,
    should_accumulate_out: Union[Sequence[bool], Any] = False,
) -> Pipeline:
  """Wraps body function in a custom pipeline defined by grid and specs.

  This has the same semantics as pallas_call but is meant to be called inside
  pallas_call for nesting grids. This is useful when you need to have separate
  windowing strategies for example for communication vs. computation.

  By default outputs are written to but `should_accumulate_out` can be used to
  specify which outputs we should add to instead. This is so we can reduce
  across pipeline calls within and across parent grid iterations.

  Args:
    body: Pipeline body.
    grid: Pallas grid.
    in_specs: Input block specs.
    out_specs: Output block specs.
    should_accumulate_out: Prefix-pytree of out_specs specifying which should be
      accumulated into with True.

  Returns:
    Wrapped pipelined body.
  """
  return emit_pipeline_with_allocations(
      body,
      grid=grid,
      in_specs=in_specs,
      out_specs=out_specs,
      should_accumulate_out=should_accumulate_out,
  )[0]
