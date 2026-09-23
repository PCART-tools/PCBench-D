def call_trainers(args, extra_args, train_data, server_rrefs):
    r"""
    A function that starts the trainers. Each trainer is started
    using an rpc_async request.
    Args:
        args (parser): benchmark configurations
        extra_args (dict): configurations added by the user
        train_data (list): training samples
        server_rrefs (dict): a dictionary containing server RRefs
    """
    futs = []
    for trainer_rank in range(0, args.ntrainer + args.ncudatrainer):
        trainer_name = get_name(
            trainer_rank,
            args
        )
        server_rref = None
        if server_rrefs:
            if trainer_rank >= args.ntrainer:
                server_rank = get_cuda_server_rank(args, trainer_rank)
            else:
                server_rank = get_server_rank(args, trainer_rank)
            server_rref = server_rrefs[server_rank]
        fut = rpc.rpc_async(
            trainer_name,
            run_trainer,
            args=(
                args,
                extra_args,
                train_data[trainer_rank],
                trainer_rank,
                server_rref,
            ),
            timeout=args.rpc_timeout
        )
        futs.append(fut)
    return futs
