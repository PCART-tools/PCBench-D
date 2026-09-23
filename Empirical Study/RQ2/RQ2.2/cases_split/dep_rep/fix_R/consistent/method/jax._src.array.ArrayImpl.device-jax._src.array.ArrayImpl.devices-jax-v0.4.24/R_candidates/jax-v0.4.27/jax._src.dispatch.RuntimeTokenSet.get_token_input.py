  def get_token_input(
      self, eff: core.Effect, devices: list[Device]
  ) -> core.Token:
    tok = self.current_tokens.get(eff, np.zeros(0, np.bool_))

    if isinstance(tok, core.Token):
      # The order of devices may change, so we need to reshard if necessary.
      # TODO(yueshengys): This might still be buggy in a multi-process SPMD
      # scenario. Revise the logic later. A distributed shutdown barrier inside
      # the XLA program may be needed.
      return jax.device_put(tok, jax.sharding.PositionalSharding(devices))

    # We only use replicated sharding for the first time when the token for the
    # order effect hasn't been created.
    s = jax.sharding.GSPMDSharding.get_replicated(devices)
    sharded_tok = core.Token(pxla.shard_args([s], [tok])[0])
    self.current_tokens[eff] = sharded_tok
    return sharded_tok
