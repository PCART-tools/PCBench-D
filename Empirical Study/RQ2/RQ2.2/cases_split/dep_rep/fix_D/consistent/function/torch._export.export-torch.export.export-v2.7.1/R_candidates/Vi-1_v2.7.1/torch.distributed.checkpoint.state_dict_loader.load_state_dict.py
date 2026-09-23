@deprecated(
    "`load_state_dict` is deprecated and will be removed in future versions. "
    "Please use `load` instead.",
    category=FutureWarning,
)
def load_state_dict(
    state_dict: dict[str, Any],
    storage_reader: StorageReader,
    process_group: Optional[dist.ProcessGroup] = None,
    coordinator_rank: int = 0,
    no_dist: bool = False,
    planner: Optional[LoadPlanner] = None,
) -> None:
    """This method is deprecated. Please switch to 'load'."""
    storage_reader.reset()
    with _profile():
        # TODO: test returning `load` here instead.
        return _load_state_dict(
            state_dict,
            storage_reader,
            process_group,
            coordinator_rank,
            no_dist,
            planner,
        )
