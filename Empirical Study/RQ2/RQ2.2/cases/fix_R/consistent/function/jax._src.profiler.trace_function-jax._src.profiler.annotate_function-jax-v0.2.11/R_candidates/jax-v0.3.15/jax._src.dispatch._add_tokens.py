def _add_tokens(has_unordered_effects: bool, ordered_effects: List[core.Effect],
                device: Device, input_bufs):
  tokens = [runtime_tokens.get_token(eff, device) for eff in ordered_effects]
  tokens_flat = flatten(tokens)
  input_bufs = [*tokens_flat, *input_bufs]
  def _remove_tokens(output_bufs):
    token_bufs, output_bufs = util.split_list(
        output_bufs, [has_unordered_effects + len(ordered_effects)])
    if has_unordered_effects:
      output_token_buf, *token_bufs = token_bufs
      runtime_tokens.set_output_token(device, output_token_buf)
    for eff, token_buf in zip(ordered_effects, token_bufs):
      runtime_tokens.update_token(eff, token_buf)
    return output_bufs
  return input_bufs, _remove_tokens
