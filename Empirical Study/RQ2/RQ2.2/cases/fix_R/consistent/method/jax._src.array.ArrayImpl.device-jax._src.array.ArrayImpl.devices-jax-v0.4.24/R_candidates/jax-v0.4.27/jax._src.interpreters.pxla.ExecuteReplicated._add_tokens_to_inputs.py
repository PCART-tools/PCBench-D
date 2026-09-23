  def _add_tokens_to_inputs(self, input_bufs):
    if self.ordered_effects:
      tokens = [
          dispatch.runtime_tokens.get_token_input(eff, self._local_devices)._buf
          for eff in self.ordered_effects
      ]
      input_bufs = [*tokens, *input_bufs]
    return input_bufs
