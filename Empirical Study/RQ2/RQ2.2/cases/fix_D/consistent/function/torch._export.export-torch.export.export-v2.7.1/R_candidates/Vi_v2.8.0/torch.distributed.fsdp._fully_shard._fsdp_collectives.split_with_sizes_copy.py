@torch.library.impl(lib, "split_with_sizes_copy", "Meta")
@torch.library.impl(lib, "split_with_sizes_copy", "CUDA")
@torch.library.impl(lib, "split_with_sizes_copy", "XPU")
@torch.library.impl(lib, "split_with_sizes_copy", "HPU")
@torch.library.impl(lib, "split_with_sizes_copy", "CPU")
@torch.library.impl(lib, "split_with_sizes_copy", "MTIA")
@torch.library.impl(lib, "split_with_sizes_copy", "PrivateUse1")
def split_with_sizes_copy(
    all_gather_output: torch.Tensor,
    all_gather_input_split_sizes: list[int],
    dim: int,
    out: list[torch.Tensor],
) -> None:
    torch.split_with_sizes_copy(
        all_gather_output, all_gather_input_split_sizes, dim=dim, out=out
    )
