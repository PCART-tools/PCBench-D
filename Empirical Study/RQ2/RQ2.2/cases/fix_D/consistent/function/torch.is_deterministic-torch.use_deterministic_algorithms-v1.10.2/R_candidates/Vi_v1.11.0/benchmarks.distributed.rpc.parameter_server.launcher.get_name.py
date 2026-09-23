def get_name(rank, args):
    r"""
    A function that gets the name for the rank
    argument
    Args:
        rank (int): process number in the world
        args (parser): benchmark configurations
    """
    t_count = args.ntrainer + args.ncudatrainer
    s_count = args.nserver + args.ncudaserver
    if rank < t_count:
        return f"trainer{rank}"
    elif rank < (t_count + s_count):
        return f"server{rank}"
    else:
        return "master"
