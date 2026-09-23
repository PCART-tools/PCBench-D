@rpc.functions.async_execution
@torch.jit.script
def async_add(to: str, x: Tensor, y: Tensor) -> Future[Tensor]:
    return rpc.rpc_async(to, script_add, (x, y))
