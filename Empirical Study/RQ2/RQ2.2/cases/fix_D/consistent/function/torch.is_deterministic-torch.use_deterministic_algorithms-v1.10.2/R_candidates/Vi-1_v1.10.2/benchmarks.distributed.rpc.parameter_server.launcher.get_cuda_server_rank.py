def get_cuda_server_rank(args, rank):
    r"""
    A function that gets the cudaserver rank for
    the rank argument.
    Args:
        args (parser): benchmark configurations
        rank (int): trainer rank
    """
    s_offset = args.ntrainer + args.ncudatrainer + args.nserver
    t_index = rank - args.ntrainer
    ctps = args.ncudatrainer // args.ncudaserver
    return t_index // ctps + s_offset
