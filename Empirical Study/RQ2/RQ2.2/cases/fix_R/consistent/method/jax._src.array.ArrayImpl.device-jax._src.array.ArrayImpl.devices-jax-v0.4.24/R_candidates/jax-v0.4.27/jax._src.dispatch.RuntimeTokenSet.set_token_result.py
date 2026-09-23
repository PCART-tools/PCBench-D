  def set_token_result(self, eff: core.Effect, token: core.Token):
    self.current_tokens[eff] = token
