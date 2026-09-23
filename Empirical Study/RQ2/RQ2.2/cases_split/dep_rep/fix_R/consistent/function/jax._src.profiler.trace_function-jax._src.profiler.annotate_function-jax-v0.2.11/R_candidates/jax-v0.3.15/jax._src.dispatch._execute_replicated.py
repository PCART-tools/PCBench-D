def _execute_replicated(name: str, compiled: XlaExecutable,
                        input_handler: Optional[Callable],
                        output_buffer_counts: Sequence[int],
                        result_handler: Callable,
                        has_unordered_effects: bool,
                        ordered_effects: List[core.Effect],
                        kept_var_idx, *args):
  if has_unordered_effects or ordered_effects:
    # TODO(sharadmv): support jit-of-pmap with effects
    raise NotImplementedError(
        "Cannot execute replicated computation with effects.")
  if input_handler: raise NotImplementedError  # TODO(mattjj, dougalm)
  input_bufs = [flatten(device_put(x, device) for i, x in enumerate(args)
                        if i in kept_var_idx)
                for device in compiled.local_devices()]
  input_bufs_flip = list(unsafe_zip(*input_bufs))
  out_bufs_flat_rep = compiled.execute_sharded_on_local_devices(input_bufs_flip)
  out_flat = [bufs[0] for bufs in out_bufs_flat_rep]
  check_special(name, out_flat)
  out_bufs = unflatten(out_flat, output_buffer_counts)
  return result_handler(None, out_bufs)
