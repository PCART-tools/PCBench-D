def launch_agent(
    config: LaunchConfig,
    entrypoint: Union[Callable, str, None],
    args: List[Any],
) -> Dict[int, Any]:
    if not config.run_id:
        run_id = str(uuid.uuid4().int)
        logger.warning(f"config has no run_id, generate a new one: {run_id}")
        config.run_id = run_id

    entrypoint_name = _get_entrypoint_name(entrypoint, args)

    logger.info(
        f"Starting elastic_operator with launch configs:\n"
        f"  entrypoint       : {entrypoint_name}\n"
        f"  min_nodes        : {config.min_nodes}\n"
        f"  max_nodes        : {config.max_nodes}\n"
        f"  nproc_per_node   : {config.nproc_per_node}\n"
        f"  run_id           : {config.run_id}\n"
        f"  rdzv_backend     : {config.rdzv_backend}\n"
        f"  rdzv_endpoint    : {config.rdzv_endpoint}\n"
        f"  rdzv_configs     : {config.rdzv_configs}\n"
        f"  max_restarts     : {config.max_restarts}\n"
        f"  monitor_interval : {config.monitor_interval}\n"
        f"  log_dir          : {config.log_dir}\n"
        f"  metrics_cfg      : {config.metrics_cfg}\n"
    )

    rdzv_parameters = RendezvousParameters(
        backend=config.rdzv_backend,
        endpoint=config.rdzv_endpoint,
        run_id=config.run_id,
        min_nodes=config.min_nodes,
        max_nodes=config.max_nodes,
        **config.rdzv_configs,
    )

    agent = None
    rdzv_handler = rdzv_registry.get_rendezvous_handler(rdzv_parameters)
    master_addr, master_port = _get_addr_and_port(rdzv_parameters)
    try:
        spec = WorkerSpec(
            role=config.role,
            local_world_size=config.nproc_per_node,
            entrypoint=entrypoint,
            args=tuple(args),
            rdzv_handler=rdzv_handler,
            max_restarts=config.max_restarts,
            monitor_interval=config.monitor_interval,
            redirects=config.redirects,
            tee=config.tee,
            master_addr=master_addr,
            master_port=master_port,
        )

        cfg = metrics.MetricsConfig(config.metrics_cfg) if config.metrics_cfg else None
        metrics.initialize_metrics(cfg)

        agent = LocalElasticAgent(
            spec=spec, start_method=config.start_method, log_dir=config.log_dir
        )

        result = agent.run()
        events.record(agent.get_agent_status_event(WorkerState.SUCCEEDED))
        if result.is_failed():
            # ChildFailedError is treated specially by @record
            # if the error files for the failed children exist
            # @record will copy the first error (root cause)
            # to the error file of the launcher process.
            raise ChildFailedError(
                name=entrypoint_name,
                failures=result.failures,
            )
        else:
            return result.return_values
    except ChildFailedError:
        raise
    except Exception:
        if agent:
            events.record(agent.get_agent_status_event(WorkerState.FAILED))
        else:
            events.record(_construct_event(config))
        raise
    finally:
        rdzv_handler.shutdown()
