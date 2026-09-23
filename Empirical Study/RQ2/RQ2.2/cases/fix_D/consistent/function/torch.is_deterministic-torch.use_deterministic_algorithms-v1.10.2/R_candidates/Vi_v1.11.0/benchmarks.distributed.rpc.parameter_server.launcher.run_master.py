def run_master(rank, data, args, extra_configs, rpc_backend_options):
    r"""
    A function that runs the master process in the world. This function
    obtains remote references to initialized servers, splits the data,
    runs the trainers, and prints metrics.
    Args:
        rank (int): process number in the world
        data (list): training samples
        args (parser): benchmark configurations
        extra_configs (dict): configurations added by the user
        rpc_backend_options (rpc): configurations/options for the rpc TODO: fix
    """
    world_size = args.ntrainer + args.ncudatrainer + args.nserver + args.ncudaserver + 1
    rpc.init_rpc(
        get_name(
            rank,
            args
        ),
        rank=rank,
        world_size=world_size,
        rpc_backend_options=rpc_backend_options
    )
    server_rrefs = {}
    for i in range(
        args.ntrainer + args.ncudatrainer, world_size - 1
    ):
        server_rrefs[i] = get_server_rref(i, args, extra_configs["server_config"])
    train_data = split_list(
        list(DataLoader(data, batch_size=args.batch_size)),
        args.ntrainer + args.ncudatrainer
    )

    # warmup run the benchmark
    benchmark_warmup(
        args, extra_configs["trainer_config"], train_data, server_rrefs
    )
    # run the benchmark
    trainer_futs = call_trainers(
        args, extra_configs["trainer_config"], train_data, server_rrefs
    )
    # collect metrics and print
    metrics_printer = ProcessedMetricsPrinter()
    rank_metrics_list = wait_all(trainer_futs)
    metrics_printer.print_metrics("trainer", rank_metrics_list)
    rank_metrics_list = get_server_metrics(server_rrefs)
    metrics_printer.print_metrics("server", rank_metrics_list)
