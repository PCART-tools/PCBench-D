def DoParallel(name, *nets_or_steps):
    """
    Execute the nets or steps in parallel, waiting for all of them to finish

    Examples:
    - DoParallel('pDo', net1, net2, ..., net_n)
    - DoParallel('pDo', list_of_nets)
    - DoParallel('pDo', step1, step2, ..., step_n)
    - DoParallel('pDo', list_of_steps)
    """
    nets_or_steps = _MakeList(nets_or_steps)
    if (len(nets_or_steps) == 1 and isinstance(
            nets_or_steps[0], core.ExecutionStep)):
        return nets_or_steps[0]
    else:
        return core.scoped_execution_step(
            _get_next_step_name('DoParallel', name),
            nets_or_steps,
            concurrent_substeps=True)
