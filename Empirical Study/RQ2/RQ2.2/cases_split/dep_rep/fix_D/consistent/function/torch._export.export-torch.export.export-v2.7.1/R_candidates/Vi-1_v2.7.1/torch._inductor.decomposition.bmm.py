@register_decomposition([aten.bmm])
@pw_cast_for_opmath
def bmm(
    self: torch.Tensor,
    batch2: torch.Tensor,
) -> torch.Tensor:
    if config.coordinate_descent_tuning and self.device.type != "cpu":
        if guard_size_oblivious(self.shape[1] == 1) or guard_size_oblivious(
            batch2.shape[2] == 1
        ):
            out = (self.unsqueeze(-1) * batch2.unsqueeze(1)).sum(dim=2)
            return out
    if self.device.type == "cpu":
        if guard_size_oblivious(self.size(1) == 1) and guard_size_oblivious(
            batch2.size(-1) == 1
        ):
            counters["inductor"]["decompose_bmm"] += 1
            return torch.sum(
                self.squeeze(1) * batch2.squeeze(-1), dim=1, keepdim=True
            ).unsqueeze(1)
    return NotImplemented
