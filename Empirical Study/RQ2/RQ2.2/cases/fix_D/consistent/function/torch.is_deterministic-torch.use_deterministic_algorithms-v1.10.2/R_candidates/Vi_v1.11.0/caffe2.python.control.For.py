def For(name, nets_or_steps, iter_num):
    """
    Execute nets_or_steps iter_num times.

    Args:
    nets_or_steps: a ExecutionStep or a Net or a list of ExecutionSteps or
                   a list nets.
    iter_num:    the number times to execute the nets_or_steps.

    Returns:
    A ExecutionStep instance.
    """
    init_net = core.Net('init-net')
    iter_cnt = init_net.CreateCounter([], init_count=iter_num)
    iter_net = core.Net('For-iter')
    iter_done = iter_net.CountDown([iter_cnt])

    for_step = core.scoped_execution_step(
        _get_next_step_name('For-inner', name),
        _PrependNets(nets_or_steps, iter_net),
        should_stop_blob=iter_done)
    return Do(name + '/For',
              Do(name + '/For-init-net', init_net),
              for_step)
