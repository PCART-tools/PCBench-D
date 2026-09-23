def contiguous(
    a: Tensor, *, memory_format: torch.memory_format = torch.contiguous_format
) -> Tensor:
    torch._check(
        memory_format != torch.preserve_format,
        lambda: "preserve memory format is unsupported by the contiguous operator",
    )

    if utils.is_contiguous_for_memory_format(a, memory_format=memory_format):
        return a

    return torch.clone(a, memory_format=memory_format)
