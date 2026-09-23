def get_buffer_counts(out_avals, ordered_effects, has_unordered_effects):
  buffer_counts = [aval_to_num_buffers(aval) for aval in out_avals]
  if ordered_effects or has_unordered_effects:
    num_output_tokens = len(ordered_effects)
    # TODO(sharadmv): remove check when minimum jaxlib version is bumped
    buffer_counts = ([1] * num_output_tokens) + buffer_counts
  return buffer_counts
