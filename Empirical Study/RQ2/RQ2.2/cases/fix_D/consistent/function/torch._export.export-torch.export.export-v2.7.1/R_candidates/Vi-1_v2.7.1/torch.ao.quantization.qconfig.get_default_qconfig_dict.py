@deprecated(
    "`torch.ao.quantization.get_default_qconfig_dict` is deprecated and will be removed in "
    "a future version. Please use `torch.ao.quantization.get_default_qconfig_mapping` instead.",
    category=FutureWarning,
)
def get_default_qconfig_dict(backend="x86", version=0):
    return torch.ao.quantization.get_default_qconfig_mapping(backend, version).to_dict()
