@torch.jit.script
def rref_to_here(rref_var: RRef[Tensor]) -> Tensor:
    return rref_var.to_here()
