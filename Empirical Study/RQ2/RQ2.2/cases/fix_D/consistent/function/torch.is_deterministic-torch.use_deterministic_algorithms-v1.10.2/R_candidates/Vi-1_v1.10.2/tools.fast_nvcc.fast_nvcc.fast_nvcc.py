def fast_nvcc(
    args: List[str],
    *,
    config: argparse.Namespace = default_config,
) -> int:
    """
    Emulate the result of calling the given nvcc binary with args.

    Should run faster than plain nvcc.
    """
    warn_if_windows()
    warn_if_tmpdir_flag(args)
    dryrun_data = nvcc_dryrun_data(config.nvcc, args)
    env = dryrun_data['env']
    warn_if_tmpdir_set(env)
    commands = dryrun_data['commands']
    if not config.faithful:
        commands = make_rm_force(unique_module_id_files(commands))

    if contains_non_executable(commands):
        return wrap_nvcc(args, config)

    command_parts = list(map(shlex.split, commands))
    if config.verbose:
        print_verbose_output(
            env=env,
            commands=command_parts,
            filename=config.verbose,
        )
    graph = nvcc_data_dependencies(commands)
    warn_if_not_weakly_connected(graph)
    if config.graph:
        print_dot_graph(
            commands=command_parts,
            graph=graph,
            filename=config.graph,
        )
    if config.sequential:
        graph = straight_line_dependencies(commands)
    results = asyncio.run(run_graph(  # type: ignore[attr-defined]
        env=env,
        commands=commands,
        graph=graph,
        gather_data=bool(config.table),
        save=config.save,
    ))
    print_command_outputs(results)
    if config.table:
        write_log_csv(command_parts, results, filename=config.table)
    return exit_code([dryrun_data] + results)
