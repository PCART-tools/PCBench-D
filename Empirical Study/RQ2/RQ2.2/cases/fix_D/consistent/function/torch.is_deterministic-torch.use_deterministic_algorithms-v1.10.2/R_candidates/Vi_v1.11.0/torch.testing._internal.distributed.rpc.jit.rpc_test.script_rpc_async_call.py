@torch.jit.script
def script_rpc_async_call(
    dst_worker_name: str, args: Tuple[Tensor, Tensor], kwargs: Dict[str, Tensor]
):
    fut = rpc.rpc_async(dst_worker_name, two_args_two_kwargs, args, kwargs)
    ret = fut.wait()
    return ret
