@register_decomposition([aten.mm])
@pw_cast_for_opmath
def mm(
    self: torch.Tensor,
    input2: torch.Tensor,
) -> torch.Tensor:
    # Our matrix vector multiplies only achieve peak bandwidth with coordinate descent tuning.
    # todo: Look into why and fix it (hopefully)
    if config.coordinate_descent_tuning and self.device.type != "cpu":
        if guard_size_oblivious(self.shape[0] == 1) or guard_size_oblivious(
            input2.shape[1] == 1
        ):
            return (self.unsqueeze(2) * input2.unsqueeze(0)).sum(dim=1)
    if self.device.type == "cpu":
        if (
            guard_size_oblivious(self.size(-1) == 1)
            and guard_size_oblivious(self.size(0) > 0)
            and guard_size_oblivious(input2.size(0) == 1)
            and (self.dtype == input2.dtype)
            and definitely_true((torch.numel(self) + torch.numel(input2)) <= 32)
        ):
            counters["inductor"]["decompose_mm"] += 1
            return torch.cat([self[i, :] * input2 for i in range(self.size(0))])
        if guard_size_oblivious(self.size(0) == 1) and guard_size_oblivious(
            input2.size(-1) == 1
        ):
            counters["inductor"]["decompose_mm"] += 1
            return torch.sum(
                self.squeeze(0) * input2.squeeze(-1), dim=0, keepdim=True
            ).unsqueeze(0)
    return NotImplemented
