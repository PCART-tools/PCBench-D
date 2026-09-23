def construct_v(output, batch_size):
    return torch.randn(batch_size, *output.shape,
                       dtype=output.dtype, device=output.device)
