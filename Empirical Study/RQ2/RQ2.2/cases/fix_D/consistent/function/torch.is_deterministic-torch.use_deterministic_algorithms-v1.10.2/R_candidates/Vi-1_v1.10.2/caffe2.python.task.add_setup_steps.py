def add_setup_steps(step, init_nets, exit_nets, name):
    if not init_nets and not exit_nets:
        return step
    steps = []
    if init_nets:
        steps.append(core.execution_step('%s:init' % name, init_nets))
    steps.append(step)
    if len(exit_nets) > 0:
        steps.append(core.execution_step('%s:exit' % name, exit_nets))
    return core.execution_step(name, steps)
