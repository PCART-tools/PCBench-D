def get_server_rank(args, rank):
    r"""
    A function that gets the server rank for
    the rank argument.
    Args:
        args (parser): benchmark configurations
        rank (int): trainer rank
    """
    s_offset = args.ntrainer + args.ncudatrainer
    tps = args.ntrainer // args.nserver
    return rank // tps + s_offset
