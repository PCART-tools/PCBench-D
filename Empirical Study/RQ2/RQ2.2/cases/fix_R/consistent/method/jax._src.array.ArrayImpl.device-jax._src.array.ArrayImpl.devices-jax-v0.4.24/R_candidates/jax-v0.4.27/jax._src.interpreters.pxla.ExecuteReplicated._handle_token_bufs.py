  def _handle_token_bufs(self, token_bufs, sharded_token):
    # token_bufs: Sequence[Sequence[tokenArray]], for each effect the returned
    # token buffers.
    # sharded_token: ShardedToken, containing the RuntimeTokens for each device
    for i, device in enumerate(self._local_devices):
      dispatch.runtime_tokens.set_output_runtime_token(
          device, sharded_token.get_token(i))
    for eff, token_buf in zip(self.ordered_effects, token_bufs):
      assert len(token_buf) > 0
      if len(token_buf) == 1:
        dispatch.runtime_tokens.set_token_result(eff, core.Token(token_buf[0]))
      else:
        token_devices = []
        for token in token_buf:
          assert isinstance(token.sharding, sharding_impls.SingleDeviceSharding)
          token_devices.append(token.sharding._device_assignment[0])
        s = sharding_impls.PositionalSharding(token_devices)
        global_token_array = jax.make_array_from_single_device_arrays(
            (0,), s, token_buf
        )
        dispatch.runtime_tokens.set_token_result(
            eff, core.Token(global_token_array)
        )
