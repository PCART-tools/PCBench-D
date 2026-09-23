def Switch(name, *conditions):
    """
    Execute the steps for which the condition is true.
    Each condition is a tuple (condition_blob_or_net, nets_or_steps).
    Note:
      1. Multi steps can be executed if their conditions are true.
      2. The conditions_blob_or_net (if it is Net) of all steps will be
         executed once.

    Examples:
    - Switch('name', (cond_1, net_1), (cond_2, net_2), ..., (cond_n, net_n))
    - Switch('name', [(cond_1, net1), (cond_2, net_2), ..., (cond_n, net_n)])
    - Switch('name', (cond_1, net_1))
    """
    conditions = _MakeList(conditions)
    return core.scoped_execution_step(
        _get_next_step_name('Switch', name),
        [_RunOnceIf(name + '/Switch', cond, step) for cond, step in conditions])
