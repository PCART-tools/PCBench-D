  def __call__(self, axis_size, all_in_batched, *all_args):
    _, args = all_args
    consts_batched, in_batched = all_in_batched
    assert not any(tree_util.tree_leaves(consts_batched)), consts_batched
    return call_rule(self.rule, axis_size, in_batched, args)
