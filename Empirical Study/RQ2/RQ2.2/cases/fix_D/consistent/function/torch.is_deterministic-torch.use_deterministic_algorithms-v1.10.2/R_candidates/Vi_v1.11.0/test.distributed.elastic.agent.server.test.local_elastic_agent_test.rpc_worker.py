def rpc_worker():
    init_rpc("worker", BackendType.TENSORPIPE)
    rpc.shutdown()
