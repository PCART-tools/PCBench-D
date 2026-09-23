def execution_step(default_name,
                   steps_or_nets,
                   num_iter=None,
                   report_net=None,
                   report_interval=None,
                   concurrent_substeps=None,
                   should_stop_blob=None,
                   only_once=None,
                   num_concurrent_instances=None,
                   create_workspace=False,
                   run_every_ms=None):
    """
    Helper for creating an ExecutionStep.
    - steps_or_nets can be:
      - None
      - Net
      - ExecutionStep
      - list<Net>
      - list<ExecutionStep>
    - should_stop_blob is either None or a scalar boolean blob.
      - This blob is checked AFTER every substeps/subnets.
      - If specified and true, then this step will return immediately.
      - Be sure to handle race conditions if setting from concurrent threads.
    - if no should_stop_blob or num_iter is provided, defaults to num_iter=1
    """
    assert should_stop_blob is None or num_iter is None, (
        'Cannot set both should_stop_blob and num_iter.')
    if should_stop_blob is None and num_iter is None:
        num_iter = 1

    step = ExecutionStep(default_name)
    if should_stop_blob is not None:
        step.SetShouldStopBlob(should_stop_blob)
    if num_iter is not None:
        step.SetIter(num_iter)
    if only_once is not None:
        step.SetOnlyOnce(only_once)
    if concurrent_substeps is not None:
        step.SetConcurrentSubsteps(concurrent_substeps)
    if report_net is not None:
        assert report_interval is not None
        step.SetReportNet(report_net, report_interval)
    if num_concurrent_instances is not None:
        step.SetNumConcurrentInstances(num_concurrent_instances)
    if create_workspace:
        step.SetCreateWorkspace(True)
    if run_every_ms:
        step.RunEveryMillis(run_every_ms)

    if isinstance(steps_or_nets, ExecutionStep):
        step.AddSubstep(steps_or_nets)
    elif isinstance(steps_or_nets, Net):
        step.AddNet(steps_or_nets)
    elif isinstance(steps_or_nets, list):
        if all(isinstance(x, Net) for x in steps_or_nets):
            for x in steps_or_nets:
                step.AddNet(x)
        else:
            for x in steps_or_nets:
                step.AddSubstep(to_execution_step(x))
    elif steps_or_nets:
        raise ValueError(
            'steps_or_nets must be a step, a net, or a list of nets or steps.')
    return step
