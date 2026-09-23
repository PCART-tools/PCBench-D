def get_server_metrics(server_rrefs):
    r"""
    A function that calls the remote server to obtain metrics
    collected during the benchmark run.
    Args:
        server_rrefs (dict): a dictionary containing server RRefs
    """
    rank_metrics = []
    for rank, server_rref in server_rrefs.items():
        metrics = server_rref.rpc_sync().get_metrics(server_rref)
        rank_metrics.append([rank, metrics])
    return rank_metrics
