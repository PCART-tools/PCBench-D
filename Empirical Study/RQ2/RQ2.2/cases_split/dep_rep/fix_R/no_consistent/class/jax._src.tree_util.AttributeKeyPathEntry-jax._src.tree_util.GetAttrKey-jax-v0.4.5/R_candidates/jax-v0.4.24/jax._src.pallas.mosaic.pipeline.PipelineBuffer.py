class PipelineBuffer(NamedTuple):
  """Current and next buffer indices for an input/output/accum ref."""
  current: Union[REF, jax.Array]
  next: Union[REF, jax.Array]
