@torch.library.impl(lib, "all_gather_copy_in", "CUDA")
@torch.library.impl(lib, "all_gather_copy_in", "XPU")
@torch.library.impl(lib, "all_gather_copy_in", "HPU")
@torch.library.impl(lib, "all_gather_copy_in", "CPU")
@torch.library.impl(lib, "all_gather_copy_in", "MTIA")
def all_gather_copy_in_cuda(
    all_gather_inputs: list[torch.Tensor],
    inp_split_sizes: list[int],
    all_gather_input_numel: int,
    world_size: int,
    rank: int,
    dtype: torch.dtype,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor]:
    all_gather_output = torch.empty(
        (all_gather_input_numel * world_size,), dtype=dtype, device=device
    )
    all_gather_input = all_gather_output.narrow(
        0, all_gather_input_numel * rank, all_gather_input_numel
    )
    foreach_copy_dsts = torch.split(all_gather_input, inp_split_sizes)
    with torch.no_grad():
        torch._foreach_copy_(foreach_copy_dsts, all_gather_inputs)
    return all_gather_input, all_gather_output
