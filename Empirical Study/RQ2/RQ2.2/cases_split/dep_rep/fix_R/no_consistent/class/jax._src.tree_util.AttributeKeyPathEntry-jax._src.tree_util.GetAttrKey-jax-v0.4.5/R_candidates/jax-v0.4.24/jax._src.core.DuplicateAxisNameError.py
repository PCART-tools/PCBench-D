class DuplicateAxisNameError(Exception):
  def __init__(self, var):
    self.var = var
    self.eqn = None
