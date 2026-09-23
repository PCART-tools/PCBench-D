@register_decomposition(aten.pixel_shuffle)
@out_wrapper()
def pixel_shuffle(self: Tensor, upscale_factor: int):
    torch._check(
        self.dim() >= 3,
        lambda: f"pixel_shuffle expects input to have at least 3 dimensions, but got input with {self.dim} dimension(s)",
    )
    batch = self.shape[:-3]
    C_out = self.shape[-3] // upscale_factor**2
    HW_out = (self.shape[-2] * upscale_factor, self.shape[-1] * upscale_factor)
    n = len(batch)
    B_dims = range(n)
    C_dim, r1_dim, r2_dim, H_dim, W_dim = range(n, n + 5)
    return (
        self.view(
            *batch,
            C_out,
            upscale_factor,
            upscale_factor,
            self.shape[-2],
            self.shape[-1],
        )
        .permute(*B_dims, C_dim, H_dim, r1_dim, W_dim, r2_dim)
        .reshape(*batch, C_out, *HW_out)
        .clone(memory_format=utils.suggest_memory_format(self))
    )
