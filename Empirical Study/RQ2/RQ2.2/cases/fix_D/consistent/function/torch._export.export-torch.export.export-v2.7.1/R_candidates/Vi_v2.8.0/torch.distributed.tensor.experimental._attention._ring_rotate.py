def _ring_rotate(
    block: torch.Tensor, pg: dist.ProcessGroup, send_to_next: bool
) -> torch.Tensor:
    block = block.contiguous()
    size = dist.get_world_size(pg)
    dsts = (
        list(range(1, size)) + [0]
        if send_to_next
        else [size - 1] + list(range(0, size - 1))
    )
    return ft_c.permute_tensor(block, dsts, pg)
