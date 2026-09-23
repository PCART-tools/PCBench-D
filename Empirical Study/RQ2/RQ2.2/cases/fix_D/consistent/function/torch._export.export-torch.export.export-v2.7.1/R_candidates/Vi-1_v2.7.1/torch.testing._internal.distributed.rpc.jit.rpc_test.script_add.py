@torch.jit.script
def script_add(x: Tensor, y: Tensor) -> Tensor:
    return x + y
