@torch.jit.script
def script_rpc_sync_call(
    dst_worker_name: str, args: Tuple[Tensor, Tensor], kwargs: Dict[str, Tensor]
):
    res = rpc.rpc_sync(dst_worker_name, two_args_two_kwargs, args, kwargs)
    return res
