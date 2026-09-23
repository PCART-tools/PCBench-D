def SwitchNot(name, *conditions):
    """
    Similar to Switch() but execute the steps for which the condition is False.
    """
    conditions = _MakeList(conditions)
    return core.scoped_execution_step(
        _get_next_step_name('SwitchNot', name),
        [_RunOnceIfNot(name + '/SwitchNot', cond, step)
         for cond, step in conditions])
