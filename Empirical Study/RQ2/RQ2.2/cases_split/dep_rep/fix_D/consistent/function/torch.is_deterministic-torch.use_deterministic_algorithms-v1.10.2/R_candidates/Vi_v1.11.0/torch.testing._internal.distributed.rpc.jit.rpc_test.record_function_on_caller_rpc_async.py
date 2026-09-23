@torch.jit.script
def record_function_on_caller_rpc_async(dst_worker_name: str, block: str) -> Tensor:
    t: Tensor = torch.ones(1)
    with record_function(block) as rf:
        fut1 = rpc.rpc_async(dst_worker_name, script_add_ones, (t, ))
        fut2 = rpc.rpc_async(dst_worker_name, script_add_ones, (t, ))
        res = fut1.wait() + fut2.wait()
    return res
