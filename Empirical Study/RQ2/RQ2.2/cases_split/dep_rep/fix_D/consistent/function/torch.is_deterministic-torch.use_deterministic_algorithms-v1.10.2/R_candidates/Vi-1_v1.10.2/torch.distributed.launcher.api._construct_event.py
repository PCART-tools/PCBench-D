def _construct_event(config: LaunchConfig) -> events.Event:
    metadata = {
        "rdzv_backend": config.rdzv_backend,
        "run_id": config.run_id,
        "role": config.role,
    }
    return events.Event(
        name="torch.distributed.elastic.launch_agent",
        source=events.EventSource.AGENT,
        metadata=cast(Dict[str, events.EventMetadataValue], metadata),
    )
