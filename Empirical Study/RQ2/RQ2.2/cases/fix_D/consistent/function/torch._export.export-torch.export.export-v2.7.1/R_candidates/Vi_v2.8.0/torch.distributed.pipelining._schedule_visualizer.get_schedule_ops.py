def get_schedule_ops(
    schedule: Union[str, _PipelineSchedule],
    pp_degree: int,
    num_microbatches: int,
    num_stages_per_rank: Optional[int] = None,
) -> list[list[Optional[_Action]]]:
    """
    Get all actions for a given schedule, pp_degree, and num_microbatches. The actions are returned in a list of lists
    where each inner list represents a rank and each element in the inner list represents an action.

    The schedule can be specified as a string which is passed into get_schedule_class() or a _PipelineSchedule instance.
    """

    if isinstance(schedule, str):
        schedule_class = get_schedule_class(schedule)
    elif type(schedule) == _PipelineSchedule:
        schedule_class = schedule
    else:
        raise ValueError(f"Invalid schedule: {schedule}")

    # Create a mock of the PipelineStage class
    mock_pipeline_stage = mock.create_autospec(PipelineStage, instance=True)
    # Set the return values for group_rank and group_size methods
    mock_pipeline_stage.group_rank = 0
    mock_pipeline_stage.group_size = pp_degree
    mock_pipeline_stage.submod = None

    # Check num_stages_per_rank is valid
    if issubclass(schedule_class, PipelineScheduleSingle):
        if num_stages_per_rank is None:
            num_stages_per_rank = 1
        assert num_stages_per_rank == 1
        stages = mock_pipeline_stage
        stages.num_stages = num_stages_per_rank * pp_degree
    elif issubclass(schedule_class, PipelineScheduleMulti):
        if num_stages_per_rank is None:
            num_stages_per_rank = 2
        assert num_stages_per_rank >= 2
        stages = [mock_pipeline_stage for _ in range(num_stages_per_rank)]
        for stage in stages:
            stage.num_stages = num_stages_per_rank * pp_degree

    else:
        raise ValueError(f"Invalid schedule: {schedule_class}")

    # Instantiate the schedule class
    schedule_instance = schedule_class(stages, num_microbatches)

    # Convert to List[List[_Action]]
    all_actions = []
    for rank in range(pp_degree):
        all_actions.append(schedule_instance.pipeline_order[rank])

    # Return the pipeline order
    return all_actions
