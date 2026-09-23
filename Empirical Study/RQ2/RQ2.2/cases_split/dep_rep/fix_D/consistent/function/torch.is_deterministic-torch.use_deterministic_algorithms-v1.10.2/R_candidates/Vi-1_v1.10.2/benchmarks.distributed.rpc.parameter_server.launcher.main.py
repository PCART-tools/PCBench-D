def main(args):
    r"""
    A function that creates multiple processes to run the benchmark.
    Args:
        args (parser): launcher configurations
    """
    # CPU and RPC trainer checks
    if args.ntrainer > 0 and args.ncudatrainer > 0:
        assert args.nserver > 0 and args.ncudaserver > 0
    if args.nserver > 0:
        assert args.ntrainer > 0
        assert args.ntrainer % args.nserver == 0
    if args.ncudaserver > 0:
        assert args.ncudatrainer > 0
        assert args.ncudatrainer % args.ncudaserver == 0

    world_size = (
        args.ntrainer + args.ncudatrainer + args.nserver + args.ncudaserver + 1
    )

    data = load_data(args)

    mp.spawn(
        run_benchmark,
        args=(
            args,
            data,
        ),
        nprocs=world_size,
        join=True
    )
