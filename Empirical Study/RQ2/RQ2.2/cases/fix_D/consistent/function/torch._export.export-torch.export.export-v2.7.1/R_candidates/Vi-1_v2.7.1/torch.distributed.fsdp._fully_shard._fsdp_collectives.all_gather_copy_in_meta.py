@torch.library.impl(lib, "all_gather_copy_in", "Meta")
def all_gather_copy_in_meta(
    all_gather_inputs: list[torch.Tensor],
    inp_split_sizes: list[int],
    all_gather_input_numel: int,
    world_size: int,
    rank: int,
    dtype: torch.dtype,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor]:
    all_gather_output = torch.empty(
        (all_gather_input_numel * world_size,), dtype=dtype, device="meta"
    )
    all_gather_input = all_gather_output.narrow(
        0, all_gather_input_numel * rank, all_gather_input_numel
    )
    return all_gather_input, all_gather_output
