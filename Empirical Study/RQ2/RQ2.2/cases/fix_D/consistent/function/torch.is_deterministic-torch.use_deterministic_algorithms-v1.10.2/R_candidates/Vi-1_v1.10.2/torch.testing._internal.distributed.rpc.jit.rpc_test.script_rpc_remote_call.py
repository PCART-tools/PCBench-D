@torch.jit.script
def script_rpc_remote_call(
    dst_worker_name: str, args: Tuple[Tensor, Tensor], kwargs: Dict[str, Tensor]
):
    rref_res = rpc.remote(dst_worker_name, two_args_two_kwargs, args, kwargs)
    return rref_res.to_here()
