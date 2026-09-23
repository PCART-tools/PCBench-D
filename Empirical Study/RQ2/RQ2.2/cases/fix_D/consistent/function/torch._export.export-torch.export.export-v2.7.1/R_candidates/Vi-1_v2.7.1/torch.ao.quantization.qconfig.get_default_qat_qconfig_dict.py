@deprecated(
    "`torch.ao.quantization.get_default_qat_qconfig_dict` is deprecated and will be removed in "
    "a future version. Please use `torch.ao.quantization.get_default_qat_qconfig_mapping` instead.",
    category=FutureWarning,
)
def get_default_qat_qconfig_dict(backend="x86", version=1):
    return torch.ao.quantization.get_default_qat_qconfig_mapping(
        backend, version
    ).to_dict()
