def Do(name, *nets_or_steps):
    """
    Execute the sequence of nets or steps once.

    Examples:
    - Do('myDo', net1, net2, ..., net_n)
    - Do('myDo', list_of_nets)
    - Do('myDo', step1, step2, ..., step_n)
    - Do('myDo', list_of_steps)
    """
    nets_or_steps = _MakeList(nets_or_steps)
    if (len(nets_or_steps) == 1 and isinstance(
            nets_or_steps[0], core.ExecutionStep)):
        return nets_or_steps[0]
    else:
        return core.scoped_execution_step(
            _get_next_step_name('Do', name), nets_or_steps)
