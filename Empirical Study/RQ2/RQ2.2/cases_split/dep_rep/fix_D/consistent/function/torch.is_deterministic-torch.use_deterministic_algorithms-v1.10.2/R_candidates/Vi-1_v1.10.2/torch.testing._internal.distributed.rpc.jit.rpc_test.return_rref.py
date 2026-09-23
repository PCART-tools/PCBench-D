@torch.jit.script
def return_rref(rref_var: RRef[Tensor]) -> RRef[Tensor]:
    return rref_var
