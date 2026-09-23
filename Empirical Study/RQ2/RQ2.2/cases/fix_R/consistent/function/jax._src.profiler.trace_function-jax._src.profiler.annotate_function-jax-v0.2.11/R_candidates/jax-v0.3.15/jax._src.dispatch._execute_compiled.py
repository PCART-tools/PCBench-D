def _execute_compiled(name: str, compiled: XlaExecutable,
                      input_handler: Optional[Callable],
                      output_buffer_counts: Sequence[int],
                      result_handler: Callable,
                      has_unordered_effects: bool,
                      ordered_effects: List[core.Effect],
                      kept_var_idx, *args):
  device, = compiled.local_devices()
  args, env = input_handler(args) if input_handler else (args, None)
  in_flat = flatten(device_put(x, device) for i, x in enumerate(args)
                    if i in kept_var_idx)
  if has_unordered_effects or ordered_effects:
    in_flat, token_handler = _add_tokens(has_unordered_effects, ordered_effects,
                                         device, in_flat)
  out_flat = compiled.execute(in_flat)
  check_special(name, out_flat)
  out_bufs = unflatten(out_flat, output_buffer_counts)
  if ordered_effects or has_unordered_effects:
    out_bufs = token_handler(out_bufs)
  return result_handler(env, out_bufs)
