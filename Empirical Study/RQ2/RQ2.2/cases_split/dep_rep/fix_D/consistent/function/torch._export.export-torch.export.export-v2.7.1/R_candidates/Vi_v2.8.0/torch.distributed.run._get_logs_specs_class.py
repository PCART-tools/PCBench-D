def _get_logs_specs_class(logs_specs_name: Optional[str]) -> type[LogsSpecs]:
    """
    Attempts to load `torchrun.logs_spec` entrypoint with key of `logs_specs_name` param.
    Provides plugin mechanism to provide custom implementation of LogsSpecs.

    Returns `DefaultLogsSpecs` when logs_spec_name is None.
    Raises ValueError when entrypoint for `logs_spec_name` can't be found in entrypoints.
    """
    logs_specs_cls = None
    if logs_specs_name is not None:
        eps = metadata.entry_points()
        if hasattr(eps, "select"):  # >= 3.10
            group = eps.select(group="torchrun.logs_specs")
            if group.select(name=logs_specs_name):
                logs_specs_cls = group[logs_specs_name].load()

        elif specs := eps.get("torchrun.logs_specs"):  # < 3.10
            if entrypoint_list := [ep for ep in specs if ep.name == logs_specs_name]:
                logs_specs_cls = entrypoint_list[0].load()

        if logs_specs_cls is None:
            raise ValueError(
                f"Could not find entrypoint under 'torchrun.logs_specs[{logs_specs_name}]' key"
            )

        logger.info(
            "Using logs_spec '%s' mapped to %s", logs_specs_name, str(logs_specs_cls)
        )
    else:
        logs_specs_cls = DefaultLogsSpecs

    return logs_specs_cls
