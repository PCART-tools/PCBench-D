def get_setup_nets(key, steps_or_nets, target):
    init_net = core.Net(key + '/init')
    exit_net = core.Net(key + '/exit')
    init_nets = []
    exit_nets = []
    objs = []
    for step_or_net in steps_or_nets:
        if hasattr(step_or_net, 'get_all_attributes'):
            objs += step_or_net.get_all_attributes(key)
        elif hasattr(step_or_net, 'get_attributes'):
            objs += step_or_net.get_attributes(key)
    for obj in objs:
        # these are needed in order to allow nesting of TaskGroup, which
        # is a feature not yet implemented.
        if hasattr(obj, '_setup_used') and obj._setup_used:
            continue
        if hasattr(obj, '_setup_target') and obj._setup_target != target:
            continue
        if hasattr(obj, 'setup'):
            nets = obj.setup(init_net)
            if isinstance(nets, (list, tuple)):
                init_nets += nets
            elif isinstance(nets, (core.Net, core.ExecutionStep)):
                init_nets.append(nets)
            elif nets is not None:
                raise TypeError('Unsupported type for setup: %s' % type(nets))
            obj._setup_used = True
        if hasattr(obj, 'exit'):
            nets = obj.exit(exit_net)
            if isinstance(nets, (list, tuple)):
                exit_nets += nets
            elif isinstance(nets, (core.Net, core.ExecutionStep)):
                exit_nets.append(nets)
            elif nets is not None:
                raise TypeError('Unsupported type for setup: %s' % type(nets))
            obj._setup_used = True

    if len(init_net.Proto().op) > 0:
        init_nets.insert(0, init_net)
    if len(exit_net.Proto().op) > 0:
        exit_nets.insert(0, exit_net)
    return init_nets, exit_nets
