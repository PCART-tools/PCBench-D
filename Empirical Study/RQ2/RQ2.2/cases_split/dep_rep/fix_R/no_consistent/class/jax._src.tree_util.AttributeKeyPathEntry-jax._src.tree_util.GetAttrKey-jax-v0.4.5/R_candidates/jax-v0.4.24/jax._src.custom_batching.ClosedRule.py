class ClosedRule:
  def __init__(self, rule):
    functools.update_wrapper(self, rule)
    self.rule = rule

  def __call__(self, axis_size, all_in_batched, *all_args):
    _, args = all_args
    consts_batched, in_batched = all_in_batched
    assert not any(tree_util.tree_leaves(consts_batched)), consts_batched
    return call_rule(self.rule, axis_size, in_batched, args)

  def __str__(self):
    return str(self.rule)
