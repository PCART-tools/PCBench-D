class RuntimeTokenSet(threading.local):
  tokens: Dict[core.Effect, Tuple[RuntimeToken, Device]]
  output_tokens: Dict[Device, RuntimeToken]

  def __init__(self):
    self.tokens = {}
    self.output_tokens = {}

  def get_token(self, eff: core.Effect, device: Device) -> RuntimeToken:
    if eff not in self.tokens:
      self.tokens[eff] = device_put(np.zeros(0, np.bool_), device), device
    elif self.tokens[eff][1] != device:
      (old_token,), _ = self.tokens[eff]
      old_token.aval = core.ShapedArray((0,), np.bool_)
      self.tokens[eff] = device_put(old_token, device), device
    return self.tokens[eff][0]

  def update_token(self, eff: core.Effect, token: RuntimeToken):
    self.tokens[eff] = token, self.tokens[eff][1]

  def set_output_token(self, device: Device, token: RuntimeToken):
    # We're free to clobber the previous output token because on each
    # device we have a total ordering of computations. Only the token
    # from the latest computation matters. If this weren't the case
    # we'd need to store a set of output tokens.
    self.output_tokens[device] = token

  def clear(self):
    self.tokens = {}
    self.output_tokens = {}

  def block_until_ready(self):
    for t, _ in self.tokens.values():
      t[0].block_until_ready()
    # TODO(sharadmv): use a runtime mechanism to block on computations instead
    # of using output tokens.
    for t in self.output_tokens.values():
      t[0].block_until_ready()
