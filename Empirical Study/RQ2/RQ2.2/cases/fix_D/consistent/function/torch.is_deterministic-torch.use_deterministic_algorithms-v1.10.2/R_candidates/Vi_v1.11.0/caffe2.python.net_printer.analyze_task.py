@Analyzer.register(Task)
def analyze_task(analyzer, task):
    # check that our plan protobuf is not too large (limit of 64Mb)
    step = task.get_step()
    plan = Plan(task.node)
    plan.AddStep(step)
    proto_len = len(plan.Proto().SerializeToString())
    assert proto_len < 2 ** 26, (
        'Due to a protobuf limitation, serialized tasks must be smaller '
        'than 64Mb, but this task has {} bytes.' % proto_len)

    is_private = task.workspace_type() != WorkspaceType.GLOBAL
    with analyzer.set_workspace(do_copy=is_private):
        analyzer(step)
