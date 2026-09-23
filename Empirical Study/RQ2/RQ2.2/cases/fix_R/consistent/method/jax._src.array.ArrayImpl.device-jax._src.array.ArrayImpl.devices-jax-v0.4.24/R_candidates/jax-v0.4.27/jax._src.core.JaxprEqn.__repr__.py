  def __repr__(self):
    return str(pp_eqn(self, JaxprPpContext(), JaxprPpSettings())).rstrip()
