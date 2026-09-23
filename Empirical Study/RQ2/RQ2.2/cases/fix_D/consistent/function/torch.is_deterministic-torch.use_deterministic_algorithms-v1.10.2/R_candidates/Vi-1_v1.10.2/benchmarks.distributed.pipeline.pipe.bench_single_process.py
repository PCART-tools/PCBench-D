def bench_single_process(args):
    os.environ.update({"MASTER_ADDR" : args.host})
    os.environ.update({"MASTER_PORT" : "10638"})

    rpc.init_rpc(
        "worker",
        rank=0,
        world_size=1,
    )

    num_devices = torch.cuda.device_count() if torch.cuda.is_available() else 1
    num_devices = min(args.num_devices, num_devices)
    assert num_devices > 0
    init_random_seed(0)
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

    blob = make_model_and_data(args, None)
    model = blob["model"]

    balance = generate_balance(num_devices, len(model))
    model = partition_model(model, balance)
    p = Pipe(
        model, chunks=args.chunks, checkpoint=args.checkpoint
    )
    del model
    del blob["model"]

    train(blob["data"], p, blob["criterion"], blob["optimizer"], blob["vocab_size"], args)
