def _get_step_context(step):
    proto = step.Proto()
    if proto.should_stop_blob:
        return call('loop'), False
    if proto.num_iter and proto.num_iter != 1:
        return call('loop', [proto.num_iter]), False
    if proto.num_concurrent_instances > 1:
        return (
            call('parallel',
                 [('num_instances', proto.num_concurrent_instances)]),
            len(step.Substeps()) > 1)
    concurrent = proto.concurrent_substeps and len(step.Substeps()) > 1
    if concurrent:
        return call('parallel'), True
    if proto.report_net:
        return call('run_once'), False
    return None, False
