@Printer.register(ExecutionStep)
def print_step(text, step):
    proto = step.Proto()
    step_ctx, do_substep = _get_step_context(step)
    with text.context(step_ctx):
        if proto.report_net:
            with text.context(call('report_net', [proto.report_interval])):
                text(step.get_net(proto.report_net))
        substeps = step.Substeps() + [step.get_net(n) for n in proto.network]
        for substep in substeps:
            sub_proto = (
                substep.Proto() if isinstance(substep, ExecutionStep) else None)
            if sub_proto is not None and sub_proto.run_every_ms:
                substep_ctx = call(
                    'reporter',
                    [str(substep), ('interval_ms', sub_proto.run_every_ms)])
            elif do_substep:
                title = (
                    'workspace'
                    if sub_proto is not None and sub_proto.create_workspace else
                    'step')
                substep_ctx = call(title, [str(substep)])
            else:
                substep_ctx = None
            with text.context(substep_ctx):
                text(substep)
                if proto.should_stop_blob:
                    text.add(call('yield stop_if', [proto.should_stop_blob]))
