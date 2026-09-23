@rpc.functions.async_execution
@torch.jit.script
def async_wrong_type() -> Tensor:
    return torch.zeros(2)
