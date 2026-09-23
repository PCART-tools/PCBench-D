def RunPlanInBackground(plan_or_step):
    # TODO(jiayq): refactor core.py/workspace.py to avoid circular deps
    import caffe2.python.core as core
    if isinstance(plan_or_step, core.ExecutionStep):
        plan_or_step = core.Plan(plan_or_step)
    return C.run_plan_in_background(StringifyProto(plan_or_step))
