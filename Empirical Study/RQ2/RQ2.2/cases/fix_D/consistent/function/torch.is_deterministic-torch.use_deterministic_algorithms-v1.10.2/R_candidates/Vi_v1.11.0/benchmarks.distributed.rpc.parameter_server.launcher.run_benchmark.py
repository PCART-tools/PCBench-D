def run_benchmark(rank, args, data):
    r"""
    A function that runs the benchmark.
    Args:
        rank (int): process number in the world
        args (parser): configuration args
        data (list): training samples
    """

    config = load_extra_configs(args)

    torch.manual_seed(args.torch_seed)
    torch.cuda.manual_seed_all(args.cuda_seed)
    torch.backends.cudnn.benchmark = True
    torch.backends.cudnn.deterministic = True

    world_size = args.ntrainer + args.ncudatrainer + args.nserver + args.ncudaserver + 1
    os.environ['MASTER_ADDR'] = args.master_addr
    os.environ['MASTER_PORT'] = args.master_port
    rpc_backend_options = TensorPipeRpcBackendOptions(rpc_timeout=args.rpc_timeout)
    if rank == world_size - 1:
        # master = [ntrainer + ncudatrainer + nserver + ncudaserver, ntrainer + ncudatrainer + nserver + ncudaserver]
        run_master(rank, data, args, config, rpc_backend_options)
    elif rank >= args.ntrainer + args.ncudatrainer:
        # parameter_servers = [ntrainer + ncudatrainer, ntrainer + ncudatrainer + nserver + ncudaserver)
        rpc.init_rpc(
            get_name(
                rank,
                args
            ),
            rank=rank,
            world_size=world_size,
            rpc_backend_options=rpc_backend_options
        )
    else:
        # trainers = [0, ntrainer + ncudatrainer)
        if rank >= args.ntrainer:
            server_rank = get_cuda_server_rank(args, rank)
            server_name = get_name(server_rank, args)
            rpc_backend_options.set_device_map(
                server_name,
                {rank: server_rank}
            )
        trainer_name = get_name(
            rank,
            args
        )
        rpc.init_rpc(
            trainer_name,
            rank=rank,
            world_size=world_size,
            rpc_backend_options=rpc_backend_options
        )
    rpc.shutdown()
