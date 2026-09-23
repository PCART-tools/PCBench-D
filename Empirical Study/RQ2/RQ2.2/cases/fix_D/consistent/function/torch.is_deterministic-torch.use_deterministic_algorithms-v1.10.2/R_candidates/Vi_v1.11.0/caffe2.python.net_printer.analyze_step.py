@Analyzer.register(ExecutionStep)
def analyze_step(analyzer, step):
    proto = step.Proto()
    with analyzer.set_workspace(do_copy=proto.create_workspace):
        if proto.report_net:
            with analyzer.set_workspace(do_copy=True):
                analyzer(step.get_net(proto.report_net))
        all_new_blobs = set()
        substeps = step.Substeps() + [step.get_net(n) for n in proto.network]
        for substep in substeps:
            with analyzer.set_workspace(
                    do_copy=proto.concurrent_substeps) as ws_in:
                analyzer(substep)
                if proto.should_stop_blob:
                    analyzer.need_blob(proto.should_stop_blob)
            if proto.concurrent_substeps:
                new_blobs = set(viewkeys(ws_in)) - set(viewkeys(analyzer.workspace))
                assert len(all_new_blobs & new_blobs) == 0, (
                    'Error: Blobs created by multiple parallel steps: %s' % (
                        ', '.join(all_new_blobs & new_blobs)))
                all_new_blobs |= new_blobs
    for x in all_new_blobs:
        analyzer.define_blob(x)
