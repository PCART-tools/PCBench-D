def _add_tokens(has_unordered_effects: bool, ordered_effects: List[core.Effect],
                has_host_callbacks: bool, device: Device, input_bufs):
  tokens = [runtime_tokens.get_token(eff, device) for eff in ordered_effects]
  tokens_flat = flatten(tokens)
  input_bufs = [*tokens_flat, *input_bufs]
  def _remove_tokens(output_bufs, runtime_token):
    num_output_tokens = len(ordered_effects)
    token_bufs, output_bufs = util.split_list(output_bufs, [num_output_tokens])
    if has_unordered_effects or has_host_callbacks:
      runtime_tokens.set_output_runtime_token(device, runtime_token)
    for eff, token_buf in zip(ordered_effects, token_bufs):
      runtime_tokens.update_token(eff, token_buf)
    return output_bufs
  return input_bufs, _remove_tokens
