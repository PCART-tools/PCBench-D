  def __init__(self, rule):
    functools.update_wrapper(self, rule)
    self.rule = rule
