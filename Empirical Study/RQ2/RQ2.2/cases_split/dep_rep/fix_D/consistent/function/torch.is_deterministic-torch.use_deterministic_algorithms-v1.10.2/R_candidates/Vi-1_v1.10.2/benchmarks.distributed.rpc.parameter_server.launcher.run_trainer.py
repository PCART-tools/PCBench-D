def run_trainer(
    args, extra_args, data, rank, server_rref
):
    r"""
    A function that runs obtains a trainer instance and calls
    the train method.
    Args:
        args (parser): benchmark configurations
        extra_args (dict): configurations added by the user
        data (list): training samples
        rank (int): process number in the world
        server_rrefs (dict): a dictionary containing server RRefs
    """
    trainer_class = trainer_map[args.trainer]
    if extra_args is not None:
        trainer_args = extra_args.values()
    else:
        trainer_args = []
    trainer_count = args.ntrainer + args.ncudatrainer
    store = c10d.FileStore(args.filestore, trainer_count)
    if args.backend == "gloo":
        process_group = c10d.ProcessGroupGloo(
            store, rank, trainer_count
        )
    elif args.backend == "nccl":
        process_group = c10d.ProcessGroupNCCL(
            store, rank, trainer_count
        )
    elif args.backend == "multi":
        process_group = c10d.ProcessGroupNCCL(
            store, rank, trainer_count
        )
        if c10d.is_initialized() is False:
            c10d.init_process_group(backend="gloo", rank=rank, world_size=trainer_count)

    model = load_model(args)
    preprocess_data = preprocess_data_map[args.preprocess_data]
    create_criterion = criterion_map[args.create_criterion]
    create_ddp_model = ddp_model_map[args.create_ddp_model]
    iteration_step = iteration_step_map[args.iteration_step]
    hook_state_class = hook_state_map[args.hook_state]
    hook = ddp_hook_map[args.ddp_hook]
    # check if this a cudatrainer
    use_cuda_rpc = rank >= args.ntrainer
    trainer = trainer_class(
        process_group,
        use_cuda_rpc,
        server_rref,
        args.backend,
        args.epochs,
        preprocess_data,
        create_criterion,
        create_ddp_model,
        hook_state_class,
        hook,
        iteration_step,
        *trainer_args
    )
    trainer.train(model, data)
    metrics = trainer.get_metrics()
    return [rank, metrics]
