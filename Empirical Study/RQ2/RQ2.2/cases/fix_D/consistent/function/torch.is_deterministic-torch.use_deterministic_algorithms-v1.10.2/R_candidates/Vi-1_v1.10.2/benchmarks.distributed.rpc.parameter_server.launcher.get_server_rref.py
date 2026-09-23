def get_server_rref(server_rank, args, extra_args):
    r"""
    A function that creates a RRef to the server.
    Args:
        server_rank (int): process number in the world
        args (parser): benchmark configurations
        extra_args (dict): configurations added by the user
    """
    server = server_map[args.server]
    name = get_name(
        server_rank,
        args
    )
    if extra_args is not None:
        server_args = extra_args.values()
    else:
        server_args = []
    if server_rank >= args.ntrainer + args.ncudatrainer + args.nserver:
        trainer_count = args.ncudatrainer / args.ncudaserver
        use_cuda_rpc = True
    else:
        trainer_count = args.ntrainer / args.nserver
        use_cuda_rpc = False
    return rpc.remote(
        name,
        server,
        args=(
            server_rank,
            trainer_count,
            use_cuda_rpc,
            *server_args,
        ),
    )
