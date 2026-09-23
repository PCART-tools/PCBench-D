def _RunOnceIf(name, condition_blob_or_net, nets_or_steps):
    """
    Execute nets_or_steps once if condition_blob_or_net evaluates as true.

    If condition_blob_or_net is Net, the condition is its last external_output
    that must be a single bool. And this net will be executed before
    nets_or_steps so as to get the condition.
    """
    condition_not_net, stop_blob = NotNet(condition_blob_or_net)
    if isinstance(condition_blob_or_net, core.Net):
        nets_or_steps = _PrependNets(
            nets_or_steps, condition_blob_or_net, condition_not_net)
    else:
        nets_or_steps = _PrependNets(nets_or_steps, condition_not_net)

    def if_step(control_name):
        return core.scoped_execution_step(
            _get_next_step_name(control_name, name),
            nets_or_steps,
            should_stop_blob=stop_blob,
            only_once=True,
        )

    if _IsNets(nets_or_steps):
        bool_net = BoolNet((stop_blob, False))
        return Do(name + '/_RunOnceIf',
                  bool_net, if_step('_RunOnceIf-inner'))
    else:
        return if_step('_RunOnceIf')
