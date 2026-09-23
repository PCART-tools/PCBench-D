def rpc_master(msg):
    init_rpc("master", BackendType.TENSORPIPE)
    ret = rpc.rpc_sync(to="worker", func=_echo, args=(msg,))
    rpc.shutdown()
    return f"{ret} from worker"
