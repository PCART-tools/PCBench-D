@register_decomposition([aten.addmm])
@pw_cast_for_opmath
def addmm(
    self: torch.Tensor,
    mat1: torch.Tensor,
    mat2: torch.Tensor,
    beta: torch.types.Number = 1,
    alpha: torch.types.Number = 1,
) -> torch.Tensor:
    if self.device.type == "cpu":
        if guard_size_oblivious(mat1.size(0) == 1) and guard_size_oblivious(
            mat2.size(-1) == 1
        ):
            counters["inductor"]["decompose_addmm"] += 1
            out = torch.sum(
                mat1.squeeze(0) * mat2.squeeze(-1), dim=0, keepdim=True
            ).unsqueeze(0)
            return alpha * out + beta * self
        if (
            guard_size_oblivious(mat1.size(0) == 1)
            and definitely_true(mat2.size(0) <= 16)
            and definitely_true(mat2.size(1) <= 16)
        ):
            counters["inductor"]["decompose_addmm"] += 1
            out = (mat1.T * mat2).sum(dim=0, keepdim=True)
            return alpha * out + beta * self
    return NotImplemented
