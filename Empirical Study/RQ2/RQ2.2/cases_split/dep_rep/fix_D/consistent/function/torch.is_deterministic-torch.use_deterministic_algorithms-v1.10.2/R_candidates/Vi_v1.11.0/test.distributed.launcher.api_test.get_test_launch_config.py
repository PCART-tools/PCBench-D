def get_test_launch_config(
    rdzv_endpoint: str,
    min_nodes: int,
    max_nodes: int,
    nproc_per_node: int,
    run_id: str = "",
    rdzv_backend: str = "etcd",
    config: Optional[Dict[str, Any]] = None,
) -> LaunchConfig:
    rdzv_configs = {}
    if config:
        rdzv_configs.update(config)
    return LaunchConfig(
        min_nodes=min_nodes,
        max_nodes=max_nodes,
        nproc_per_node=nproc_per_node,
        run_id=run_id,
        rdzv_endpoint=rdzv_endpoint,
        monitor_interval=1,
        rdzv_backend=rdzv_backend,
        start_method="spawn",
        max_restarts=0,
        rdzv_configs=rdzv_configs,
    )
