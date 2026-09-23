@torch.library.impl(lib, "chunk_cat", "Meta")
@torch.library.impl(lib, "chunk_cat", "CUDA")
@torch.library.impl(lib, "chunk_cat", "XPU")
@torch.library.impl(lib, "chunk_cat", "HPU")
@torch.library.impl(lib, "chunk_cat", "CPU")
@torch.library.impl(lib, "chunk_cat", "MTIA")
def chunk_cat(
    tensors: list[torch.Tensor],
    dim: int,
    num_chunks: int,
    out: torch.Tensor,
) -> None:
    torch._chunk_cat(tensors, dim, num_chunks, out=out)
