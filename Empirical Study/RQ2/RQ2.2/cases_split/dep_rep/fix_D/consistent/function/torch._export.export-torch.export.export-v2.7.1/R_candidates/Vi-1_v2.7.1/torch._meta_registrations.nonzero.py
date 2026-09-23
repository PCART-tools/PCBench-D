@register_meta([torch.ops.aten.nonzero.default, torch.ops.aten.nonzero.out])
@out_wrapper()
def nonzero(self):
    torch._check_not_implemented(
        exp_config.meta_nonzero_assume_all_nonzero,
        lambda: "The register_meta function for torch.nonzero() raises unimplemented by default, "
        "as a correct data-independent implementation does not exist. This implementation "
        "returns a fake value, assuming all elements of the tensor are non-zero. "
        "To enable this registration, please set "
        "'torch.fx.experimental._config.meta_nonzero_assume_all_nonzero' to True.",
    )
    return torch.empty_strided(
        (self.numel(), self.dim()),
        (1, self.numel()),
        dtype=torch.long,
        device=self.device,
    )
