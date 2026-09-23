def benchmark_warmup(
    args, extra_args, data, server_rrefs
):
    r"""
    A function that runs the training algorithm. The goal of this
    function is to warm the rpc. The server states are reset.
    Args:
        args (parser): benchmark configurations
        extra_args (dict): configurations added by the user
        data (list): training samples
        server_rrefs (dict): a dictionary containing server RRefs
    """
    futs = call_trainers(args, extra_args, data, server_rrefs)
    wait_all(futs)
    for server_rref in server_rrefs.values():
        server_rref.rpc_sync().reset_state(server_rref)
    print("benchmark warmup done\n")
